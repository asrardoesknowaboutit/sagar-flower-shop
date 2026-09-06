"""Create responsive web copies of supplied media; originals remain untouched."""
from pathlib import Path
import json,subprocess
from PIL import Image,ImageOps
ROOT=Path(__file__).resolve().parents[1]
files=sorted((ROOT/'assets/images').glob('*.jpeg'))
names=[('brand','Sagar Flower Shop logo','सागर फूल सेंटर'),('brand','Sagar Flower Shop logo alternate','सागर फूल सेंटर'),('bouquets','Rose embrace','गुलाबांचा गुच्छ'),('bouquets','A blush-pink surprise','गुलाबी फुलांची भेट'),('bouquets','Ruby rose bouquet','लाल गुलाबांचा गुच्छ'),('bouquets','Pretty in pink','गुलाबी फुलांचा गुच्छ'),('bouquets','A grand floral gesture','फुलांची खास भेट'),('bouquets','Blush rose bouquet','गुलाबी गुलाब'),('decor','Marigold celebration stage','झेंडूची स्टेज सजावट'),('decor','A canopy of flowers','पलंग सजावट'),('decor','Golden haldi swing','हळदीचा झोपाळा'),('belts','Rose & jasmine waist belt','फुलांचा कंबरपट्टा'),('bouquets','A little rose romance','गुलाबांची खास भेट'),('decor','Rose wedding bed','पलंग सजावट'),('bouquets','A rainbow of flowers','रंगीबेरंगी फुलांचा गुच्छ'),('garlands','Colourful celebration garland','रंगीबेरंगी हार'),('bouquets','Classic red roses','लाल गुलाबांचा गुच्छ'),('bouquets','Three hearts, all roses','गुलाबांची मांडणी'),('bouquets','The garden bouquet','मिश्र फुलांचा गुच्छ'),('bouquets','Freshly gathered','ताज्या फुलांचा गुच्छ'),('garlands','Rose & ivory wedding garland','गुलाबांचा लग्नहार'),('garlands','Traditional rose garland','पारंपरिक हार'),('garlands','Marigold celebration garland','झेंडूचा हार'),('decor','A grand floral welcome','फुलांची भव्य सजावट'),('decor','A colourful wedding ride','गाडी सजावट'),('garlands','Golden marigold garland','झेंडूचा हार'),('garlands','Crimson & pearl garland','खास लग्नहार'),('decor','Rose-petal wedding car','गुलाबांची गाडी सजावट'),('decor','A heart of flowers','गाडी सजावट'),('decor','The grand wedding arrival','लग्नाची गाडी सजावट'),('garlands','For the biggest celebrations','भव्य स्वागत हार'),('bouquets','A bouquet to remember','फुलांची आठवणीतली भेट'),('garlands','The grand celebration garland','भव्य फुलांचा हार'),('belts','Rose & jasmine gajra','गुलाब आणि मोगऱ्याचा गजरा'),('bouquets','A cascade of roses','गुलाबांचा खास गुच्छ'),('bouquets','An evening in bloom','फुलांची खास भेट')]
labels={'bouquets':'Bouquets','garlands':'Wedding garlands','decor':'Celebration décor','belts':'Floral jewellery'}
items=[]
for n,(p,(category,title,marathi)) in enumerate(zip(files,names)):
 im=ImageOps.exif_transpose(Image.open(p)).convert('RGB')
 if category=='brand':
  if n==0:
   im.thumbnail((420,220));im.save(ROOT/'assets/brand/sagar-logo.webp',quality=90,method=6)
  continue
 folder=ROOT/'assets/images'/category;folder.mkdir(exist_ok=True)
 stem=f'collection-{n:02d}';copies={}
 for size,quality in [(360,76),(640,81),(1280,85)]:
  small=im.copy();small.thumbnail((size,size*2));dest=folder/f'{stem}-{size}.webp';small.save(dest,quality=quality,method=6);copies[str(size)]={'path':str(dest.relative_to(ROOT)),'width':small.width,'height':small.height}
 items.append(dict(id=f'new-{n}',title=title,marathi=marathi,category=category,label=labels[category],src=copies['1280']['path'],thumb=copies['640']['path'],width=copies['1280']['width'],height=copies['1280']['height'],copies=copies,source=p.name))
old=json.loads((ROOT/'assets/portfolio.json').read_text())
for i in old:
 if i['id'] in [25,37,31,19,48,44]:
  i['id']=f"original-{i['id']}";i['marathi']={'bouquets':'फुलांची खास भेट','decor':'फुलांची सजावट'}[i['category']];i['label']=labels[i['category']];items.append(i)
(ROOT/'assets/collection.json').write_text(json.dumps(items,ensure_ascii=False,indent=2))
video_titles=[('delivery','Flowers, on their way','जवळच्या परिसरात डिलिव्हरी'),('rose-varmala','The wedding edit','लग्नहारांची खास झलक'),('lotus-varmala','A beautiful beginning','शुभमंगल क्षणांसाठी')]
videos=[]
for source,(stem,title,mr) in zip(sorted((ROOT/'assets/images').glob('*.mp4')),video_titles):
 dest=ROOT/'assets/videos'/f'{stem}.mp4';poster=ROOT/'assets/videos'/f'{stem}-poster.webp'
 subprocess.run(['ffmpeg','-v','error','-i',str(source),'-c:v','copy','-an','-movflags','+faststart','-y',str(dest)],check=True)
 subprocess.run(['ffmpeg','-v','error','-ss','1','-i',str(source),'-frames:v','1','-vf','scale=480:-2','-quality','80','-y',str(poster)],check=True)
 videos.append(dict(id=stem,title=title,marathi=mr,src=str(dest.relative_to(ROOT)),poster=str(poster.relative_to(ROOT)),bytes=dest.stat().st_size))
(ROOT/'assets/videos.json').write_text(json.dumps(videos,ensure_ascii=False,indent=2))
print('Created',len(items),'designs and',len(videos),'videos; video bytes:',sum(i['bytes'] for i in videos))
