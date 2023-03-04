import requests;
from bs4 import BeautifulSoup;
import re;
import networkx as nx;
import threading;

REQ_R = re.compile(r"erequisites?..(.*)$");
CLASS_R = re.compile(r"(\b[A-Z]*\s?\d{3}[A-Z]?\b)");

CPREF_R = r"rpResults_ctl";
CNUM_R = r"_lblCNum";
CTITLE_R = r"_lblTitle";
CCO_R = r"_lblCoLocated";
CDESC_R = r"_lblDesc";

fine = ['2TEM', '7DGD', '7DOM', '7DOR', '7DPD', '7DPR', '7DPS', '7PHM', '7TMJ', 'AAAS', 'ACC', 'ACM', 'ACY', 'AEC', 'AH', 'AHST', 'ALC', 'AME', 'AMST', 'AMU', 'ANA', 'ANR', 'ANTH', 'APS', 'ARBC', 'ASLA', 'ASTR', 'ATHS', 'BCH', 'BCSC', 'BCSC', 'BIOL', 'BME', 'BPH', 'BPP', 'BRN', 'BSI', 'BSN', 'BST', 'BUS', 'BVC', 'CASC', 'CED', 'CGRK', 'CHB', 'CHE', 'CHEM', 'CHIN', 'CIS', 'CIS', 'CL', 'CLST', 'CLTR', 'CMP', 'CMT', 'CND', 'CSC', 'CSSP', 'CTSC', 'CVS', 'CVSC', 'DANC', 'DBL', 'DCD', 'DEN', 'DGD', 'DH', 'DMST', 'DOM', 'DOR', 'DPD', 'DPR', 'DPS', 'DSCC', 'DSCC', 'DTR', 'EAP', 'EAS', 'ECE', 'ECM', 'ECMS', 'ECON', 'ED', 'EDD', 'EDE', 'EDF', 'EDU', 'EESC', 'EHUM', 'EI', 'EIC', 'ELP', 'ENGL', 'ENS', 'ENT', 'ERG', 'ESL', 'ESM', 'ESMGR', 'ETH', 'EUP', 'EXP', 'FIN', 'FIN', 'FL', 'FMST', 'FR', 'FREN', 'FS', 'FWS', 'GBA', 'GEN', 'GER', 'GHOC', 'GPR', 'GREK', 'GRMN', 'GSW', 'GSW', 'GSWS', 'GTC', 'GTR', 'HBRW', 'HIS', 'HIST', 'HLSC', 'HP', 'HPC', 'HRN', 'HRP', 'HSE', 'HSM', 'HUM', 'IEP', 'IND', 'INS', 'INTD', 'INTR', 'IT', 'ITAL', 'JAZ', 'JCM', 'JPNS', 'JWST', 'KBD', 'KORE', 'LAM', 'LATN', 'LAW', 'LAW', 'LING', 'LTST', 'LUT', 'MATH', 'MBI', 'ME', 'MED', 'MGC', 'MHB', 'MHS', 'MIF', 'MKT', 'ML', 'MSC', 'MSM', 'MTL', 'MUE', 'MUSC', 'MUSC', 'MUY', 'NAVS', 'NLX', 'NSC', 'NSCI', 'NSCI', 'NSG', 'NUR', 'NURGR', 'OB', 'OMG', 'OP', 'OPT', 'ORB', 'ORC', 'ORG', 'OSH', 'PA', 'PCL', 'PEC', 'PED', 'PHIL', 'PHL', 'PHLT', 'PHP', 'PHYS', 'PHYS', 'PIC', 'PM', 'POLS', 'PORT', 'PPC', 'PPHE', 'PRC', 'PRF', 'PSC', 'PSCI', 'PSI', 'PSY', 'PSYC', 'PTH', 'RAD', 'REL', 'RELC', 'RSST', 'RUS', 'RUSS', 'SAB', 'SABR', 'SART', 'SAX', 'SENR', 'SKRT', 'SMU', 'SOCI', 'SPAN', 'STAT', 'STR', 'STR', 'STRG', 'SUST', 'TBA', 'TBN', 'TCS', 'TEB', 'TEC', 'TEE', 'TEM', 'TEO', 'TH', 'THE', 'TME', 'TMJ', 'TOX', 'TPT', 'TURK', 'VCC', 'VCE', 'VCL', 'VLA', 'VLN', 'VSR', 'WKS', 'WLN', 'WMST', 'WMT', 'WRTG', 'WSEGR', 'WST'];
replacements = {
    "STT": "STAT",
    "MTH": "MATH",
    "AST": "ASTR",
    "PHY": "PHYS",
    "BCS": "BCSC",
    "MUR": "MUSC",
    "BIO": "BIOL",
    "CHM": "CHEM",
    "CLT": "CLTR",
    "ECO": "ECON",
    "ENG": "ENGL",
    "LAT": "LATN",
    "KOR": "KORE",
    "LIN": "LING",
    "PH": "PHLT",
    "POR": "PORT",
    "PSC": "PSCI",
    "RUS": "RUSS",
    "SOC": "SOCI",
    "SP": "SPAN",
    "WRT": "WRTG",
}
REPL_R = re.compile('|'.join(replacements.keys())+'|'+'|'.join(replacements.values())+'|'+'|'.join(fine), re.IGNORECASE);

with open("./data/ALLLECTURES.html", 'r') as f:
    soup = BeautifulSoup(f.read(), features="html.parser");

desc = soup.find("span", {"id": re.compile(CPREF_R + "2317" + CDESC_R)})

# N_COURSES = len(soup.find_all("span", {"id": re.compile(CPREF_R + r"[0-9]+" + CNUM_R)} ));
# print(N_COURSES);
N_COURSES = 1936;

# GRAPH
G = nx.Graph();

for i in range(0,N_COURSES):
    ctlIndex = 2 * i + 1;
    try:
        name = soup.find("span", {"id": re.compile(CPREF_R + f'{ctlIndex:02}' + CNUM_R)}).text
        dept = name.split(" ")[0];
        name = name.replace(" ", "").split("-")[0];
        title = soup.find("span", {"id": re.compile(CPREF_R + f'{ctlIndex:02}' + CTITLE_R)}).text;
        desc = soup.find("span", {"id": re.compile(CPREF_R + f'{ctlIndex:02}' + CDESC_R)}).text;
        
        # prereq = re.search(REQ_R, desc).group(1);

        G.add_node(name, title=title, description=desc, dept=dept);
        
        desc = title + ": " + desc;
        desc = re.sub(REPL_R, lambda ele: ele.group(0).upper(), desc);

        # if prereq:
        curpref = "";
        for match in re.finditer(CLASS_R, desc):
            reqclass = match.group(1).replace(" ", "").upper().strip();
            if not reqclass.isnumeric() and reqclass[-1] != 'H':
                curpref = re.sub("\d", "", reqclass).strip();
            elif re.sub("\d", "", reqclass) == "OR":
                reqclass = curpref + reqclass.strip().removeprefix("OR").strip();
            else:
                reqclass = curpref + reqclass;
            reqclass = reqclass.replace(" ", "");
            reqpref = re.sub("\d", "", reqclass);
            if reqpref not in fine and reqpref in replacements:
                reqclass = re.sub(reqpref, replacements.get(reqpref), reqclass);
                # print(f"!! replaced {reqpref} with {replacements.get(reqpref)} !!");
            if G.has_edge(reqclass, name):
                G[reqclass][name]['weight'] += 1;
            else:
                G.add_edge(reqclass, name, weight=1);
            # print(f"Prereq: {reqclass} weight {G[reqclass][name]}");
        
        print(f"{threading.current_thread().getName()}: =========== {name} =========== {len(G.nodes)} nodes and {len(G.edges)} edges.");
        
    except AttributeError:
        continue;

nx.write_graphml(G, "./classgraph.graphml");