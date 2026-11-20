#!/bin/sh
# Archive material for "What Happened to Kannapolis?" — all public domain, CC0 or CC BY (licences logged in SOURCES.jsonl).
# Large scans are fetched as renditions (Special:FilePath ?width=…) to keep raw/ small.
cd "$(dirname "$0")/.." || exit 1
PY=${PY:-python}
F="$PY tools/footage.py fetch"
big() {   # name, file title, credit, licence, width
  [ -f "raw/$1.jpg" ] && return 0
  enc=$($PY -c "import sys,urllib.parse;print(urllib.parse.quote(sys.argv[1].replace(' ','_')))" "$2")
  $F "https://commons.wikimedia.org/wiki/Special:FilePath/$enc?width=${5:-2600}" --name "$1" \
    --page "https://commons.wikimedia.org/wiki/File:$enc" --license "$4" --credit "$3"
}
H="Lewis W. Hine, National Child Labor Committee, 1912 (Library of Congress)"
big hine_parker "The Logical Conclusion of the Lassez (i.e., Laissez) Faires Policy. Herman Parker, said six years old, and he and others said he had worked in the Cannon Mills, Kannapolis, N.C. LOC nclc.02646.jpg" "$H" "Public domain"
big hine_school "A group of children attending the public school, Kannapolis, N.C., every one of which said he or she had worked in the Cotton Mills there. The two smallest boys said ten years old. LOC nclc.02638.jpg" "$H" "Public domain"
big hine_otie "The three on the ground work in the Cannon Mills, Concord, N.C. The boy 'Otie Honeycott' (his mother could not spell his name) said he had been doffing two years in the Cannon Mill. LOC nclc.02649.jpg" "$H" "Public domain"
big hine_boys "A few of the young boys working in the Cannon Mills, Concord, N.C., but only a few of them and not the smallest. LOC nclc.02654.jpg" "$H" "Public domain"
big hine_housing "Some of the housing conditions of the workers in the Cannon Mills, Concord, N.C., to contrast with the homes and gardens some times shown from the 'show mills' of the state. LOC nclc.02651.jpg" "$H" "Public domain"
big eleanor_ymca "Eleanor Roosevelt at YMCA in Kannapolis, North Carolina - NARA - 196166.jpg" "National Archives (NAID 196166)" "Public domain"
big postcard_mill "Cannon mills postcard.jpg" "Postcard, Cannon Mills" "Public domain" 1232
big postcard_kmill "Cannon Mills, Kannapolis, N. C. (5811472491).jpg" "Postcard via Flickr (CC BY 2.0)" "CC BY 2.0" 1500
big postcard_church "First Presbyterian Church, Kannapolis, N. C. (5812037012).jpg" "Postcard via Flickr (CC BY 2.0)" "CC BY 2.0" 1500
big pillowtex_offices "Main offices of the Pillowtex Corporation, shortly before demolition in July 2005.jpg" "Wikimedia Commons, 2005" "Public domain" 1710
big pillowtex_2003 "Pillowtex Corporation.JPG" "Wikimedia Commons" "Public domain" 640
big implosion "Canon mills implosion.jpg" "Wikimedia Commons" "Public domain" 320
big westave_now "West Avenue, Kannapolis 2.jpg" "Wikimedia Commons (CC0)" "CC0 1.0" 2600
for p in 0001 0002 0010; do big "sanborn1926_$p" "Sanborn Fire Insurance Map from Kannapolis, Rowan And Cabarrus Counties, North Carolina, 1926, Plate $p.jpg" "Sanborn Map Company, 1926 (Library of Congress)" "Public domain" 3200; done
for p in 0001 0006 0011; do big "sanborn1943_$p" "Sanborn Fire Insurance Map from Kannapolis, Rowan And Cabarrus Counties, North Carolina, 1943, Plate $p.jpg" "Sanborn Map Company, 1943 (Library of Congress)" "Public domain" 3200; done
# batch 2
big charles_cannon "Charles Albert Cannon circa 1920.jpg" "Charles A. Cannon, c. 1920" "Public domain" 746
big campus1 "Kannapolis Research Campus building 01.jpg" "Wikimedia Commons (CC0)" "CC0 1.0" 2600
big campus2 "Kannapolis Research Campus building 02.jpg" "Wikimedia Commons (CC0)" "CC0 1.0" 2000
big strike1934 "Troops Attack Textile Strikers with Bullets, Bayonets and Tear Gas Daily Worker September 22, 1934.png" "Daily Worker, 22 September 1934" "Public domain" 1350
big towel_looms "Towel Looms (12671086685).jpg" "Flickr (CC BY 2.0)" "CC BY 2.0" 2600
[ -f raw/mill1920.webm ] || $F commons:"File:Filature et Tissage du coton (1920).webm" --name mill1920
