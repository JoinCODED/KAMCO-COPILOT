"""Re-theme every built page to the CODED brand palette (navy + blue), from coded-reels-playbook :root."""
import re, glob
M = {
 # accent ramp red -> CODED blue
 "#C8324A": "#2F74D6", "#E0566E": "#6F9CE8", "#EC8B9C": "#A8C2F0", "#5D181A": "#0A3A80", "#8B1E2A": "#004AA3",
 "#D03A52": "#2F74D6", "#A52439": "#004AA3", "#E66B82": "#6F9CE8", "#F4A6B5": "#A8C2F0", "#FBDDE3": "#DCE7FA",
 "#CF3850": "#2F74D6", "#D23A52": "#2F74D6", "#7E1F2C": "#0B4A9E", "#7C1E2C": "#0B4A9E", "#9A1F2C": "#0B4A9E",
 "#3A0D14": "#0B2350", "#3C0D17": "#0B2350", "#F2A0AF": "#A8C2F0", "#F3DDE2": "#DCE7FA",
 # surfaces warm black -> navy
 "#0A0507": "#00081C", "#150A0D": "#0A1630", "#1C0E12": "#11244A", "#130A0C": "#0B1833", "#190E11": "#10203F",
 "#241019": "#16294A", "#240A11": "#0D1E44", "#120A0C": "#0B1A36", "#170C0F": "#0E1D3B", "#070509": "#00081C",
 "#060304": "#000614", "#0C0810": "#00081C", "#140C13": "#0B1833", "#1C1019": "#11244A", "#241622": "#16294A",
 "#33212C": "#22375E", "#48303C": "#2E4774", "#5E4250": "#3B5684", "#080509": "#00081C", "#110B0F": "#0A1630",
 "#100A0E": "#0A1630", "#0F0A0E": "#071228", "#0A060A": "#071228", "#0A0608": "#00081C", "#140A0D": "#0A1630",
 "#1B0E12": "#11244A", "#160B0E": "#0D1A36",
 # ink warm grey -> CODED cool grey
 "#F5F0F1": "#F3F6FC", "#AEA2A5": "#9FB2D4", "#76696C": "#6F83A8", "#FBF7F8": "#F5F8FD", "#E4DBDF": "#D6E0F2",
 "#B6A9AE": "#9FB2D4", "#83767E": "#6F83A8", "#5B4E56": "#4D6086", "#F8F3F4": "#F5F8FD", "#B7AAAD": "#9FB2D4", "#7E7074": "#6F83A8",
}
R = {"200,50,74": "47,116,214", "208,58,82": "47,116,214", "224,86,110": "111,156,232", "230,107,130": "111,156,232",
     "123,30,40": "0,74,163", "93,24,26": "0,40,100", "139,30,42": "0,74,163", "132,38,96": "62,80,221",
     "10,5,7": "0,8,28", "30,14,18": "12,26,56", "6,3,4": "0,6,20", "8,5,7": "0,8,28", "8,5,9": "0,8,28",
     "14,8,12": "4,14,34", "20,10,13": "10,22,48", "5,4,7": "0,6,20"}
HEX = re.compile(r"#[0-9A-Fa-f]{6}\b")
RGB = re.compile(r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)")


def fix(t):
    parts = re.split(r"(data:[a-z/+]+;base64,[A-Za-z0-9+/=]+)", t)
    for i in range(0, len(parts), 2):
        p = HEX.sub(lambda m: M.get(m.group(0).upper(), m.group(0)), parts[i])
        p = RGB.sub(lambda m: m.group(0).split("(")[0] + "(" + R.get("%s,%s,%s" % m.groups(), "%s,%s,%s" % m.groups()), p)
        parts[i] = p
    return "".join(parts)


if __name__ == "__main__":
    for f in glob.glob("out/site/*.html") + glob.glob("out/facilitator/*.html"):
        t = open(f, encoding="utf-8").read(); open(f, "w", encoding="utf-8").write(fix(t))
    print("rebranded")
