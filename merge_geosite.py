import geosite_pb2

def read_geosite(file_path):
    db = geosite_pb2.GeoSiteList()
    with open(file_path, 'rb') as f:
        db.ParseFromString(f.read())
    return db

def merge_geosites(original, custom):
    seen = set()
    for site in original.entry:
        seen.update((d.type, d.value) for d in site.domain)

    for site in custom.entry:
        for d in site.domain:
            if (d.type, d.value) not in seen:
                # Добавляем в первую группу
                original.entry[0].domain.append(d)
                seen.add((d.type, d.value))

def write_geosite(db, file_path):
    with open(file_path, 'wb') as f:
        f.write(db.SerializeToString())

def main():
    original = read_geosite('original_geosite.dat')
    custom = read_geosite('custom_geosite.dat')

    merge_geosites(original, custom)

    write_geosite(original, 'config/binary/geosite/geosite.dat')

if __name__ == '__main__':
    main()
