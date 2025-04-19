import os
import geosite_pb2

def read_geosite(file_path):
    db = geosite_pb2.GeoSiteList()
    with open(file_path, 'rb') as f:
        db.ParseFromString(f.read())
    return db

def merge_geosites(original, custom):
    existing_category_codes = {site.country_code for site in original.entry}

    for site in custom.entry:
        if site.country_code not in existing_category_codes:
            original.entry.append(site)
            existing_category_codes.add(site.country_code)
        else:
            # Если категория уже есть, то можно объединять домены
            target_site = next(s for s in original.entry if s.country_code == site.country_code)
            existing_domains = set((d.type, d.value) for d in target_site.domain)
            for d in site.domain:
                if (d.type, d.value) not in existing_domains:
                    target_site.domain.append(d)
                    existing_domains.add((d.type, d.value))

def write_geosite(db, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'wb') as f:
        f.write(db.SerializeToString())

def main():
    original = read_geosite('original_geosite.dat')
    custom = read_geosite('custom_geosite.dat')

    merge_geosites(original, custom)

    write_geosite(original, 'config/binary/geosite/geosite.dat')

if __name__ == '__main__':
    main()
