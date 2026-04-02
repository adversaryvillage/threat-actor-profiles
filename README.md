# Threat Actor Profiles

An open-source, community-driven threat actor and adversary profiles, reusable artwork, interactive attack path diagrams, detection engineering, adversary emulation plans, and threat intelligence references.

**Built by [Adversary Village](https://adversaryvillage.org)** | **Live at [threatactors.adversaryvillage.org](https://threatactors.adversaryvillage.org)**

---

## The Story Behind This Project

This project started from something simple - I was creating threat actor artwork and emulation plans for a few APT groups as part of our work at [Adversary Village](https://adversaryvillage.org). We needed quality visuals for conference talks, training sessions, and our community content. I put together a few actor profiles with custom artwork, mapped their TTPs, wrote up emulation guidance, and realized there was nothing like this that existed as a single, open, reusable resource.

There are plenty of places to read about threat actors - MITRE ATT&CK, vendor reports, CISA advisories, blog posts scattered across dozens of sites. But there's no single place where you get the full picture in one page: who they are, what they use, how they attack, how to emulate them, how to detect them, and how to defend against them - all sourced, all linked, all free to use.

That's what this project is. And it's open to everyone.

---

## Why This Exists

### Free threat actor profiles for the community

Every profile on this site - the artwork, the data, the diagrams - is free for anyone to use in their projects, conference talks, training materials, workshops, or research. If you're building a presentation on APT29 and need a clean profile page to reference, it's here. If you're running a training session on ransomware actors and need a visual breakdown of FIN7's attack chain, it's here. No paywalls, no vendor lock-in, no login required.

The threat intelligence community produces incredible research, but it's fragmented across hundreds of vendor blogs, government advisories, and academic papers. This project brings it together into structured, consistent, actionable profiles that anyone can use and anyone can improve.

### A practical guide to emulating threat actors

The second goal is equally important - we want this to be the go-to resource for understanding how to emulate these threat actors in your own environment. Every profile includes an "Emulation Plans & Guidance" section with direct links to:

- **Step-by-step emulation walkthroughs** from blogs and research papers that show you exactly how to replicate the actor's TTPs
- **Open-source emulation plans** from MITRE CTID, Attack Arsenal, and community GitHub repos with Caldera abilities, payloads, and adversary profiles
- **Adversary simulation repos** with full attack chains you can run in a lab - custom C2 setups, exploit chains, persistence mechanisms
- **Vendor emulation guides** from AttackIQ, SCYTHE, and others that map the actor's techniques to validation scenarios

Whether you're a red teamer building an adversary emulation exercise, a purple team operator validating detections, or a student learning how nation-state actors operate in practice, these profiles give you everything you need to go from reading about a threat actor to actually emulating them in a controlled environment.

### Sourced, verified, actionable

Every claim on every profile is sourced. Defense recommendations cite who recommends them (CISA, NIST, NSA, Microsoft) with URLs to the actual documents. Detection rules link to the real Sigma YAML files on GitHub. References point to actual reports, not search pages. Emulation plans link to repos you can clone and run. If something doesn't have a source, it doesn't belong here.

---

## Contributors Welcome

This is a community project. We need people who can:

- **Add new threat actor profiles** - Pick an APT group not yet covered, research it, and create a JSON file
- **Create actor artwork** - Design profile images for threat actors (cyberpunk, technical, illustrative - your style)
- **Write emulation guides** - Document how to emulate a specific actor's TTPs in a lab, publish it as a blog post, and we'll link it
- **Add detection content** - Contribute Sigma rules, KQL queries, or Splunk searches mapped to specific actor techniques
- **Improve existing profiles** - Add missing references, fix broken URLs, expand descriptions, add new campaigns
- **Translate profiles** - Help make this accessible in other languages

No contribution is too small. Even fixing a single broken URL or adding one missing CVE helps.

---

## How to Contribute a New Threat Actor

### Step 1: Fork and clone

```bash
git clone https://github.com/YOUR_USERNAME/threat-actor-profiles.git
cd threat-actor-profiles
git checkout -b add-volttyphoon
```

### Step 2: Create the JSON file

Copy any existing actor as a template:

```bash
cp data/actors/apt28.json data/actors/volttyphoon.json
```

### Step 3: Fill in the data

Open `volttyphoon.json` and replace all fields. Here's the complete schema:

#### Core identity (required)

```json
{
  "id": "volttyphoon",
  "name": "Volt Typhoon",
  "aliases": ["BRONZE SILHOUETTE", "Vanguard Panda", "DEV-0391"],
  "country": "China",
  "country_code": "CN",
  "flag_emoji": "🇨🇳",
  "attribution": "PRC Ministry of State Security (MSS)",
  "motivation": "Espionage, Pre-positioning",
  "threat_type": "Nation-State",
  "first_seen": "2021",
  "last_seen": "2025",
  "status": "Active",
  "mitre_id": "G1017",
  "description": "A detailed paragraph about the actor (500+ characters recommended)..."
}
```

#### Targeting

```json
{
  "target_sectors": ["Critical Infrastructure", "Energy", "Telecommunications"],
  "target_countries": ["United States", "Guam"],
  "target_country_flags": [
    {"country": "United States", "flag": "🇺🇸"}
  ]
}
```

#### ATT&CK techniques (grouped by tactic)

```json
{
  "attack_techniques": {
    "initial_access": [{"id": "T1190", "name": "Exploit Public-Facing Application"}],
    "execution": [{"id": "T1059.001", "name": "PowerShell"}],
    "persistence": [],
    "privilege_escalation": [],
    "defense_evasion": [],
    "credential_access": [],
    "discovery": [],
    "lateral_movement": [],
    "collection": [],
    "command_and_control": [],
    "exfiltration": [],
    "impact": []
  }
}
```

#### Attack flow (interactive diagram)

```json
{
  "attack_flow": {
    "campaign": "US Critical Infrastructure (2023-2025)",
    "steps": [
      {"step": "Exploit Fortinet", "tid": "T1190", "tactic": "Initial Access", "desc": "Exploits Fortinet appliances"},
      {"step": "PowerShell LOTL", "tid": "T1059.001", "tactic": "Execution", "desc": "Uses built-in tools"}
    ]
  }
}
```

#### Diamond Model

```json
{
  "diamond_model": {
    "adversary": "PRC MSS contractors",
    "infrastructure": "Compromised SOHO routers, KV Botnet",
    "capability": "Living-off-the-land binaries, custom web shells",
    "victim": "US critical infrastructure operators"
  }
}
```

#### Tools with source URLs

```json
{
  "tools": ["Mimikatz", "China Chopper"],
  "tool_urls": [
    {"name": "Mimikatz", "url": "https://github.com/gentilkiwi/mimikatz", "type": "Credential Dumping"},
    {"name": "China Chopper", "url": "https://attack.mitre.org/software/S0020/", "type": "Web Shell"}
  ]
}
```

#### CVEs exploited

```json
{
  "cves": [
    {"id": "CVE-2024-21887", "desc": "Ivanti Connect Secure RCE", "year": "2024"}
  ]
}
```

#### Detection engineering

Link to actual Sigma rules or vendor guides:

```json
{
  "detection": [
    {
      "title": "LSASS Credential Dumping",
      "content": "Monitor lsass.exe access. Sysmon Event ID 10 with GrantedAccess 0x1010.",
      "url": "https://github.com/SigmaHQ/sigma/blob/master/rules/windows/sysmon/sysmon_cred_dump_lsass_access.yml"
    }
  ]
}
```

#### Defense recommendations

Cite the source and link to the document:

```json
{
  "defense_recommendations": [
    {
      "text": "Deploy phishing-resistant MFA (FIDO2/WebAuthn).",
      "source": "CISA AA25-141A",
      "url": "https://www.cisa.gov/news-events/cybersecurity-advisories/aa25-141a"
    }
  ]
}
```

#### Emulation plans & guidance

Only actor-specific resources. No generic framework links:

```json
{
  "emulation_plans": [
    {
      "name": "MITRE CTID - Volt Typhoon Emulation Plan",
      "source": "MITRE CTID",
      "type": "Open Source",
      "url": "https://github.com/center-for-threat-informed-defense/adversary_emulation_library/tree/master/volttyphoon",
      "desc": "Full emulation plan with LOTL techniques"
    }
  ]
}
```

Type values: `Open Source`, `Commercial`, `Blog Post`, `Guide`.

#### Attribution, threat assessment, legal actions, news

```json
{
  "attribution_confidence": {
    "level": "High",
    "evidence": [
      {"text": "CISA/NSA/FBI joint advisory", "url": "https://www.cisa.gov/..."}
    ]
  },
  "threat_assessment": {
    "capability": 8, "intent": 9, "targeting": 7,
    "overall": "Critical",
    "summary": "Summary of threat level..."
  },
  "legal_actions": [
    {"date": "2024-01", "type": "Advisory", "title": "...", "url": "https://..."}
  ],
  "recent_news": [
    {"date": "2025-01", "title": "...", "url": "https://..."}
  ]
}
```

#### References, sources, contributors

```json
{
  "references": [
    {"title": "CISA Advisory AA23-144A", "url": "https://www.cisa.gov/..."}
  ],
  "ioc_sources": [
    {"name": "CISA IOCs", "url": "https://...", "desc": "..."}
  ],
  "data_sources": [
    {"name": "MITRE ATT&CK G1017", "url": "https://attack.mitre.org/groups/G1017/"}
  ],
  "page_contributors": [
    {
      "name": "Your Name",
      "github": "https://github.com/yourhandle",
      "twitter": "https://twitter.com/yourhandle",
      "linkedin": "https://linkedin.com/in/yourhandle"
    }
  ]
}
```

### Step 4: Add artwork (optional)

Drop an image in `data/actors/images/` matching the actor ID:

```
data/actors/images/volttyphoon.png
```

Supported: `.png`, `.jpg`, `.jpeg`, `.svg`, `.webp`. If no image is provided, a placeholder with the actor's initials is shown.

### Step 5: Build and preview

```bash
python3 generate.py
python3 -m http.server 8000
# Open http://localhost:8000/volttyphoon/
```

No dependencies - Python 3 standard library only.

### Step 6: Submit the pull request

```bash
git add data/actors/volttyphoon.json
git add data/actors/images/volttyphoon.png
git commit -m "Add Volt Typhoon (G1017) threat actor profile"
git push origin add-volttyphoon
```

Open a pull request. In the PR description, include:
- Actor name and MITRE ATT&CK Group ID
- Number of references and their sources
- Any sections you were unable to fill in (it's okay to submit partial profiles - others can help complete them)

The maintainers review for accuracy and source quality, then merge.

---

## Updating an Existing Actor

Edit the JSON file in `data/actors/`, run `python3 generate.py`, and submit a PR describing what changed and why. Common updates: new campaign entries, additional CVEs, new emulation blog posts, updated references, corrected URLs.

---

## Auto-Enrichment

`enrich.py` pulls data from the MITRE ATT&CK STIX repository:

```bash
python3 enrich.py       # Downloads ATT&CK data, enriches all actors
python3 generate.py     # Rebuild with enriched data
```

This adds 30-50 references per actor, all mapped software with URLs, all technique mappings, and all known aliases.

---

## Data Quality Standards

- **References**: Direct URLs to actual reports. No search links. No generic landing pages.
- **Detection**: Link to the actual Sigma YAML, Elastic rule, or vendor guide.
- **Defense**: Cite the source (CISA, NIST, NSA, Microsoft) with a URL.
- **Tools**: GitHub repo for open-source, ATT&CK Software page for custom malware.
- **Emulation plans**: Only resources specific to that threat actor.
- **CVEs**: Documented as exploited by this actor in published reporting.
- **Attribution**: Source document required (DOJ indictment, government advisory, vendor report).

---

## Current Threat Actors

| Actor | Country | MITRE ID | Emulation Plans | References |
|-------|---------|----------|----------------|------------|
| APT28 (Fancy Bear) | Russia | G0007 | 8 | 21 |
| APT29 (Cozy Bear) | Russia | G0016 | 14 | 15 |
| APT41 (Double Dragon) | China | G0096 | 3 | 11 |
| FIN7 (Carbanak) | Russia | G0046 | 8 | 6 |
| Kimsuky | North Korea | G0094 | 5 | 6 |
| Lazarus Group | North Korea | G0032 | 7 | 15 |
| MuddyWater | Iran | G0069 | 3 | 6 |
| OilRig (APT34) | Iran | G0049 | 5 | 6 |
| Sandworm (APT44) | Russia | G0034 | 11 | 16 |
| Turla (Snake) | Russia | G0010 | 6 | 7 |

---

© 2026 [Adversary Village](https://adversaryvillage.org)

## License
Released under the [GNU General Public License v3 (GPL-3.0)](./LICENSE).



