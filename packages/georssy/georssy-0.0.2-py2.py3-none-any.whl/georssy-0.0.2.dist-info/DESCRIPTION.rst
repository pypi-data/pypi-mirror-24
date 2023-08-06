# georssy
A rough Python GeoRSS (Geographically Encoded Objects for RSS feeds) decoder.

georssy is a very rough decoder for the GeoRSS GeoRSS (Geographically Encoded Objects for RSS feeds) standard.

For information about GeoRSS: http://www.georss.org/

## How to install georssy
Currently, the repository it's the only way to use georssy.

## How to use georssy
from georssy import GeoRssDecoder
georss_entry = GeoRssDecoder( parent_node = r, polygons_over_boxes = True )
tmp = georss_entry.polygon_list

## TODO
- add url and file as decoder inputs
- Python 3
- Tests
- PIP packaging

---
# georssy is under development! So it's not so stable as you can expect! :)
---


