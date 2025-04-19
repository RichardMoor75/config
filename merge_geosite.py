import os
import geosite_pb2

def read_geosite(file_path):
    db = geosite_pb2.GeoSiteList()
    with open(file_path, 'rb') as f:
        db.ParseFromString(f.read())
    return db

def create_antifilter_category(custom):
    new_site = geosite_pb2.GeoSite()
    new_site.country_code = "antifilter-community"
    
    for site in custom.entry:
        for d in site.domain:
            domain = new_site.domain.add()
            domain.type = d.type
            domain.value = d.value

    return new_site

def merge_geosites(original, custom):
    antifilter_site = create_antifilter_category(custom)
    original.entry.append(antifilter_site)

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
