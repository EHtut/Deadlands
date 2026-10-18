"""Download every resolved MOD jar into tools/.cache/jars, verified by sha512.

    python tools/fetch_jars.py            all mods (client + both) - for check_deps
    python tools/fetch_jars.py --server <dir>   copy the server-side set (both + server) into <dir>

A file whose sha512 does not match what Modrinth published is deleted and
reported, never kept: a corrupt jar and a missing one must not look alike.
"""
import hashlib, json, pathlib, shutil, sys, urllib.request
HERE = pathlib.Path(__file__).resolve().parent
JARS = HERE / ".cache" / "jars"
sys.path.insert(0, str(HERE))
from gen_pack import side_of  # the same sidedness rules the pack uses

def sha512(p):
    h = hashlib.sha512()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()

def main():
    rows = [r for r in json.loads((HERE/".cache"/"resolved.json").read_text(encoding="utf-8"))
            if r["status"] == "RESOLVED" and r.get("kind", "mod") == "mod"]
    JARS.mkdir(parents=True, exist_ok=True)
    # A superseded jar left in the cache is still SCANNED by check_deps, so an old
    # GeckoLib sitting beside the new one can satisfy a requirement the pack no
    # longer meets. The cache holds exactly the resolved set or it lies.
    want = {r["filename"] for r in rows}
    for p in JARS.glob("*.jar"):
        if p.name not in want: p.unlink(); print("purged stale", p.name)
    bad = 0
    for r in rows:
        dest = JARS / r["filename"]
        if dest.exists() and sha512(dest) == r["sha512"]: continue
        req = urllib.request.Request(r["url"], headers={"User-Agent": "EHtut/zombiepack"})
        with urllib.request.urlopen(req, timeout=120) as s, open(dest, "wb") as f: shutil.copyfileobj(s, f)
        if sha512(dest) != r["sha512"]:
            dest.unlink(); bad += 1; print("HASH MISMATCH", r["slug"])
    print(f"{len(rows) - bad}/{len(rows)} jars verified in {JARS}")
    if "--server" in sys.argv:
        out = pathlib.Path(sys.argv[sys.argv.index("--server") + 1]); out.mkdir(parents=True, exist_ok=True)
        keep = {r["filename"] for r in rows if side_of(r) in ("both", "server")}
        for p in out.glob("*.jar"):
            if p.name not in keep: p.unlink(); print("removed", p.name)
        for name in keep: shutil.copy2(JARS / name, out / name)
        print(f"{len(keep)} server-side jars -> {out}")
    return 1 if bad else 0

if __name__ == "__main__":
    raise SystemExit(main())
