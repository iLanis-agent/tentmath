(function (root) {
  "use strict";
  var PAD_W = 65;   // labeled sleeping pad width, cm
  var PAD_L = 200;  // labeled sleeping pad length, cm
  var MARGIN = 60;  // labeled working margin each side, cm
  var PACK_CM2 = 1800; // labeled pack footprint, cm2

  function round1(x) { return Math.round(x * 10) / 10; }
  function plural(n, word, form) { return n + " " + (n === 1 ? word : (form || word + "s")); }

  function sleepPlan(floorWcm, floorLcm, rating) {
    if (!(floorWcm > 0) || !(floorLcm > 0) || !(rating > 0)) return { error: "the floor sides and the rating must be positive" };
    var capacity = floorLcm >= PAD_L ? Math.floor(floorWcm / PAD_W) : 0;
    var diff = rating - capacity;
    var verdict;
    if (diff <= 0) verdict = "the label holds";
    else if (diff === 1) verdict = "one body fewer than the label";
    else verdict = "two or more fewer than the label";
    return { capacity: capacity, verdict: verdict };
  }

  function sitePlan(tentWcm, tentLcm, siteWcm, siteLcm) {
    if (!(tentWcm > 0) || !(tentLcm > 0) || !(siteWcm > 0) || !(siteLcm > 0)) return { error: "the tent and the site sides must be positive" };
    var needW = tentWcm + 2 * MARGIN;
    var needL = tentLcm + 2 * MARGIN;
    var spare = Math.min(siteWcm - needW, siteLcm - needL);
    var verdict;
    if (spare < 0) verdict = "the site is too tight";
    else if (spare >= 100) verdict = "a roomy pitch";
    else verdict = "a workable pitch";
    return { needW: needW, needL: needL, spare: spare, verdict: verdict };
  }

  function vestPlan(depthCm, widthCm, packs) {
    if (!(depthCm > 0) || !(widthCm > 0) || !(packs > 0)) return { error: "the vestibule, the width and the packs must be positive" };
    var areaM2 = round1(depthCm * widthCm / 10000);
    var fit = Math.floor(depthCm * widthCm / PACK_CM2);
    var verdict;
    if (fit >= packs) verdict = "every pack inside";
    else if (fit === 0) verdict = "no pack fits inside";
    else verdict = "some packs inside";
    return { areaM2: areaM2, fit: fit, verdict: verdict };
  }

  function renderSleep(r, floorWcm, floorLcm, rating) {
    var capText = r.capacity === 0 ? "no labeled pads" : plural(r.capacity, "labeled pad");
    return "A floor " + floorWcm + " cm by " + floorLcm + " cm fits " + capText
      + " - rated " + rating + ", " + r.verdict + ".";
  }

  function renderSite(r, tentWcm, tentLcm, siteWcm, siteLcm) {
    return "A tent " + tentWcm + " cm by " + tentLcm + " cm with a labeled " + MARGIN + " cm margin asks "
      + r.needW + " cm by " + r.needL + " cm; the site gives " + siteWcm + " cm by " + siteLcm + " cm - " + r.verdict + ".";
  }

  function renderVest(r, depthCm, widthCm, packs) {
    var hold = r.fit >= packs
      ? (packs === 1 ? "holds the pack" : "holds all " + packs + " packs")
      : "holds " + r.fit + " of " + plural(packs, "pack");
    return "A vestibule " + depthCm + " cm by " + widthCm + " cm is a labeled " + r.areaM2 + " m2 - "
      + hold + ", " + r.verdict + ".";
  }

  var api = { sleepPlan: sleepPlan, sitePlan: sitePlan, vestPlan: vestPlan, renderSleep: renderSleep, renderSite: renderSite, renderVest: renderVest };
  if (typeof module !== "undefined" && module.exports) module.exports = api; else root.TentMath = api;
})(this);
