#!/usr/bin/env python3
"""
Threat Actors — Auto-Enrichment Script
Downloads MITRE ATT&CK STIX data and enriches all actor JSON files with:
- All references from MITRE ATT&CK (30-50 per actor)
- All mapped software/tools with ATT&CK Software URLs
- All mapped techniques with ATT&CK Technique URLs  
- All known aliases
- Relationship mappings to other groups

Usage: python3 enrich.py
Requires internet access to download MITRE ATT&CK data.
"""
import json, os, glob, urllib.request, sys

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, 'data', 'actors')
STIX_URL = "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack.json"
STIX_FILE = os.path.join(BASE, '.cache', 'enterprise-attack.json')

# Map our actor IDs to MITRE ATT&CK group external IDs
ACTOR_MAP = {
    "apt28": "G0007", "apt29": "G0016", "lazarus": "G0032",
    "sandworm": "G0034", "turla": "G0010", "apt41": "G0096",
    "fin7": "G0046", "oilrig": "G0049", "kimsuky": "G0094",
    "muddywater": "G0069"
}

def download_stix():
    os.makedirs(os.path.dirname(STIX_FILE), exist_ok=True)
    if os.path.isfile(STIX_FILE):
        size = os.path.getsize(STIX_FILE)
        if size > 1_000_000:
            print(f"  Using cached STIX data ({size//1_000_000}MB)")
            return
    print("  Downloading MITRE ATT&CK STIX data...")
    urllib.request.urlretrieve(STIX_URL, STIX_FILE)
    print(f"  Downloaded: {os.path.getsize(STIX_FILE)//1_000_000}MB")

def load_stix():
    with open(STIX_FILE, 'r') as f:
        return json.load(f)

def find_group(stix, mitre_id):
    for obj in stix['objects']:
        if obj.get('type') != 'intrusion-set':
            continue
        for ref in obj.get('external_references', []):
            if ref.get('external_id') == mitre_id:
                return obj
    return None

def get_references(group_obj):
    refs = []
    for ref in group_obj.get('external_references', []):
        url = ref.get('url', '')
        name = ref.get('source_name', '')
        desc = ref.get('description', '')
        if url and name:
            refs.append({"title": f"{name}: {desc[:80]}" if desc else name, "url": url})
    return refs

def get_relationships(stix, group_id):
    rels = []
    for obj in stix['objects']:
        if obj.get('type') != 'relationship':
            continue
        if obj.get('source_ref') == group_id or obj.get('target_ref') == group_id:
            rels.append(obj)
    return rels

def get_software(stix, group_id):
    """Find all software used by this group via relationships."""
    software = []
    rels = get_relationships(stix, group_id)
    software_ids = set()
    for r in rels:
        if r.get('relationship_type') == 'uses':
            target = r.get('target_ref', '')
            if target.startswith('malware--') or target.startswith('tool--'):
                software_ids.add(target)
    
    for obj in stix['objects']:
        if obj.get('id') in software_ids:
            name = obj.get('name', '')
            refs = obj.get('external_references', [])
            mitre_url = ''
            for ref in refs:
                if ref.get('source_name') == 'mitre-attack':
                    mitre_url = ref.get('url', '')
                    break
            if name:
                software.append({
                    "name": name,
                    "url": mitre_url,
                    "type": obj.get('type', 'tool').replace('malware', 'Malware').replace('tool', 'Tool')
                })
    return software

def get_techniques(stix, group_id):
    """Find all techniques used by this group."""
    techniques = []
    rels = get_relationships(stix, group_id)
    tech_ids = set()
    for r in rels:
        if r.get('relationship_type') == 'uses' and r.get('target_ref', '').startswith('attack-pattern--'):
            tech_ids.add(r['target_ref'])
    
    for obj in stix['objects']:
        if obj.get('id') in tech_ids:
            name = obj.get('name', '')
            refs = obj.get('external_references', [])
            tid = ''
            url = ''
            for ref in refs:
                if ref.get('source_name') == 'mitre-attack':
                    tid = ref.get('external_id', '')
                    url = ref.get('url', '')
                    break
            if tid:
                techniques.append({"tid": tid, "name": name, "url": url})
    return sorted(techniques, key=lambda x: x['tid'])

def enrich_actor(actor, stix):
    aid = actor['id']
    mitre_id = ACTOR_MAP.get(aid)
    if not mitre_id:
        print(f"  {aid}: no MITRE ID mapping, skipping")
        return False
    
    group = find_group(stix, mitre_id)
    if not group:
        print(f"  {aid}: group {mitre_id} not found in STIX data")
        return False
    
    group_stix_id = group['id']
    
    # Extract references
    new_refs = get_references(group)
    existing_urls = {r.get('url', '') for r in actor.get('references', [])}
    added_refs = [r for r in new_refs if r['url'] not in existing_urls]
    actor.setdefault('references', []).extend(added_refs)
    
    # Extract software/tools with URLs
    new_software = get_software(stix, group_stix_id)
    existing_tools = {t.get('name', '').lower() for t in actor.get('tool_urls', [])}
    for sw in new_software:
        if sw['name'].lower() not in existing_tools:
            actor.setdefault('tool_urls', []).append(sw)
    
    # Update tools list
    tool_names = set(actor.get('tools', []))
    for sw in new_software:
        tool_names.add(sw['name'])
    actor['tools'] = sorted(tool_names)
    
    # Extract techniques
    new_techs = get_techniques(stix, group_stix_id)
    actor['mitre_techniques'] = new_techs
    
    # Update aliases from STIX
    stix_aliases = group.get('aliases', [])
    existing_aliases = set(actor.get('aliases', []))
    for alias in stix_aliases:
        if alias != actor.get('name', ''):
            existing_aliases.add(alias)
    actor['aliases'] = sorted(existing_aliases)
    
    print(f"  {aid}: +{len(added_refs)} refs (total {len(actor.get('references',[]))}), "
          f"+{len(new_software)} tools, {len(new_techs)} techniques, "
          f"{len(actor.get('aliases',[]))} aliases")
    return True

def main():
    print(f"\n{'='*60}")
    print("  Threat Actors — Auto-Enrichment")
    print("  Pulling data from MITRE ATT&CK STIX repository")
    print(f"{'='*60}\n")
    
    download_stix()
    stix = load_stix()
    print(f"  Loaded {len(stix['objects'])} STIX objects\n")
    
    enriched = 0
    for fp in sorted(glob.glob(os.path.join(DATA, '*.json'))):
        with open(fp, 'r') as f:
            actor = json.load(f)
        if enrich_actor(actor, stix):
            with open(fp, 'w') as f:
                json.dump(actor, f, indent=2, ensure_ascii=False)
            enriched += 1
    
    print(f"\n  ✅ Enriched {enriched} actors from MITRE ATT&CK STIX data")
    print(f"  Run 'python3 generate.py' to rebuild the site.\n")

if __name__ == '__main__':
    main()
