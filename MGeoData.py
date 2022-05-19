import geoip2
import geoip2.database

cityReader = geoip2.database.Reader('dbip-city-lite.mmdb')
asnReader = geoip2.database.Reader('dbip-asn-lite.mmdb')
