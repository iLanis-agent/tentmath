import json, math

def jsnum(x):
    return int(x) if isinstance(x, float) and x == int(x) else x
def plural(n, word, form=None): return str(jsnum(n)) + " " + (word if n == 1 else (form or word + "s"))
def fmt(x): return str(jsnum(x))
def round1(x): return jsnum(math.floor(x * 10 + 0.5) / 10)

PAD_W = 65
PAD_L = 200
MARGIN = 60
PACK_CM2 = 1800

def sleep_plan(floorWcm, floorLcm, rating):
    if not (floorWcm > 0) or not (floorLcm > 0) or not (rating > 0):
        return {"error": "the floor sides and the rating must be positive"}
    capacity = math.floor(floorWcm / PAD_W) if floorLcm >= PAD_L else 0
    diff = rating - capacity
    if diff <= 0: verdict = "the label holds"
    elif diff == 1: verdict = "one body fewer than the label"
    else: verdict = "two or more fewer than the label"
    return {"capacity": capacity, "verdict": verdict}

def site_plan(tentWcm, tentLcm, siteWcm, siteLcm):
    if not (tentWcm > 0) or not (tentLcm > 0) or not (siteWcm > 0) or not (siteLcm > 0):
        return {"error": "the tent and the site sides must be positive"}
    need_w = tentWcm + 2 * MARGIN
    need_l = tentLcm + 2 * MARGIN
    spare = min(siteWcm - need_w, siteLcm - need_l)
    if spare < 0: verdict = "the site is too tight"
    elif spare >= 100: verdict = "a roomy pitch"
    else: verdict = "a workable pitch"
    return {"needW": need_w, "needL": need_l, "spare": spare, "verdict": verdict}

def vest_plan(depthCm, widthCm, packs):
    if not (depthCm > 0) or not (widthCm > 0) or not (packs > 0):
        return {"error": "the vestibule, the width and the packs must be positive"}
    area_m2 = round1(depthCm * widthCm / 10000)
    fit = math.floor(depthCm * widthCm / PACK_CM2)
    if fit >= packs: verdict = "every pack inside"
    elif fit == 0: verdict = "no pack fits inside"
    else: verdict = "some packs inside"
    return {"areaM2": area_m2, "fit": fit, "verdict": verdict}

def render_sleep(r, floorWcm, floorLcm, rating):
    cap_text = "no labeled pads" if r["capacity"] == 0 else plural(r["capacity"], "labeled pad")
    return ("A floor " + fmt(floorWcm) + " cm by " + fmt(floorLcm) + " cm fits " + cap_text
            + " - rated " + fmt(rating) + ", " + r["verdict"] + ".")

def render_site(r, tentWcm, tentLcm, siteWcm, siteLcm):
    return ("A tent " + fmt(tentWcm) + " cm by " + fmt(tentLcm) + " cm with a labeled " + fmt(MARGIN) + " cm margin asks "
            + fmt(r["needW"]) + " cm by " + fmt(r["needL"]) + " cm; the site gives " + fmt(siteWcm) + " cm by "
            + fmt(siteLcm) + " cm - " + r["verdict"] + ".")

def render_vest(r, depthCm, widthCm, packs):
    if r["fit"] >= packs:
        hold = "holds the pack" if packs == 1 else "holds all " + fmt(packs) + " packs"
    else:
        hold = "holds " + fmt(r["fit"]) + " of " + plural(packs, "pack")
    return ("A vestibule " + fmt(depthCm) + " cm by " + fmt(widthCm) + " cm is a labeled " + fmt(r["areaM2"])
            + " m2 - " + hold + ", " + r["verdict"] + ".")

cases = []
def add(fn, f, rf, args):
    r = f(*args)
    c = {"fn": fn, "args": args, "result": r}
    if "error" not in r: c["render"] = rf(r, *args)
    cases.append(c)

for a in [[260,210,4],[220,200,3],[200,210,4],[130,200,2],[150,190,2],[325,220,5],[250,210,4],[400,210,4],[0,210,4],[260,210,0]]:
    add("sleepPlan", sleep_plan, render_sleep, a)
for a in [[260,210,500,400],[260,210,380,330],[260,210,500,500],[300,300,400,400],[200,150,320,270],[260,210,480,430],[260,210,479,430],[280,220,400,500],[0,210,500,400],[260,210,500,0]]:
    add("sitePlan", site_plan, render_site, a)
for a in [[75,130,2],[60,120,4],[50,100,3],[40,90,3],[30,80,1],[20,80,1],[90,150,8],[55,110,3],[0,130,2],[75,130,0]]:
    add("vestPlan", vest_plan, render_vest, a)
json.dump(cases, open("expected.json", "w"), separators=(",", ":"))
print(len(cases), "cases")
