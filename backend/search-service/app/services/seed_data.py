# -*- coding: utf-8 -*-
"""
Seed data module - fallback data source when ES is unavailable.

Covers 6 cities (Beijing/Shanghai/Chengdu/Xi'an/Sanya/Hangzhou)
x 3 categories (attraction/hotel/restaurant), total 36 realistic POIs.
"""

_SEED_POIS: list = [
    # ========== Beijing ==========
    {
        "id": "seed_bj_001", "name": "故宫博物院", "type": "attraction",
        "city": "北京", "district": "东城区",
        "rating": 4.8, "price": 60,
        "tags": ["世界遗产", "必打卡", "历史古迹", "明清皇宫"],
        "lat": 39.9163, "lng": 116.3972,
        "address": "北京市东城区景山前街4号",
        "description": "世界现存规模最大、保存最完整的木质结构古建筑群，明清两代的皇家宫殿，被誉为世界五大宫之首。",
        "opening_hours": "08:30-17:00(旺季)/08:30-16:30(淡季)",
        "popularity_score": 98.5,
    },
    {
        "id": "seed_bj_002", "name": "天坛公园", "type": "attraction",
        "city": "北京", "district": "东城区",
        "rating": 4.7, "price": 15,
        "tags": ["世界遗产", "皇家园林", "祈年殿", "晨练"],
        "lat": 39.8822, "lng": 116.4066,
        "address": "北京市东城区天坛内东里7号",
        "description": "明清皇帝祭天祈谷的场所，祈年殿是其标志性建筑，回音壁、三音石等声学奇观亦不容错过。",
        "opening_hours": "06:00-21:00",
        "popularity_score": 92.3,
    },
    {
        "id": "seed_bj_003", "name": "八达岭长城", "type": "attraction",
        "city": "北京", "district": "延庆区",
        "rating": 4.6, "price": 40,
        "tags": ["世界遗产", "壮丽山河", "户外运动", "摄影圣地"],
        "lat": 40.3541, "lng": 116.0195,
        "address": "北京市延庆区G6京藏高速58号出口",
        "description": "万里长城最精华的段落之一，地势险峻、气势磅礴。「不到长城非好汉」即出于此。",
        "opening_hours": "07:00-18:00(旺季延至19:00)",
        "popularity_score": 96.1,
    },
    {
        "id": "seed_bj_004", "name": "北京王府井希尔顿酒店", "type": "hotel",
        "city": "北京", "district": "东城区",
        "rating": 4.7, "price": 1200,
        "tags": ["五星级", "商务出行", "市中心", "泳池"],
        "lat": 39.9150, "lng": 116.4110,
        "address": "北京市东城区王府井大街8号",
        "description": "地处王府井商圈核心，步行可达故宫、天安门，配备室内恒温泳池与米其林推荐中餐厅。",
        "opening_hours": "全天候 24h",
        "popularity_score": 88.0,
    },
    {
        "id": "seed_bj_005", "name": "胡同里·四合院民宿", "type": "hotel",
        "city": "北京", "district": "西城区",
        "rating": 4.5, "price": 380,
        "tags": ["民宿", "四合院", "胡同文化", "拍照打卡"],
        "lat": 39.9375, "lng": 116.3780,
        "address": "北京市西城区什刹海街道柳荫街24号",
        "description": "藏在后海胡同深处的百年四合院，院内枣树成荫，青砖灰瓦间感受老北京胡同生活。",
        "opening_hours": "入住 14:00 / 退房 12:00",
        "popularity_score": 79.5,
    },
    {
        "id": "seed_bj_006", "name": "大董烤鸭店(工体店)", "type": "restaurant",
        "city": "北京", "district": "朝阳区",
        "rating": 4.8, "price": 350,
        "tags": ["烤鸭", "北京菜", "宴请", "米其林"],
        "lat": 39.9305, "lng": 116.4442,
        "address": "北京市朝阳区工人体育场东门辅路",
        "description": "意境菜开创者，酥不腻烤鸭皮酥肉嫩。环境雅致，适合商务宴请与家庭聚餐。",
        "opening_hours": "11:00-14:00 / 17:00-21:30",
        "popularity_score": 95.7,
    },

    # ========== Shanghai ==========
    {
        "id": "seed_sh_001", "name": "外滩", "type": "attraction",
        "city": "上海", "district": "黄浦区",
        "rating": 4.9, "price": 0,
        "tags": ["免费", "城市地标", "夜景", "万国建筑"],
        "lat": 31.2400, "lng": 121.4900,
        "address": "上海市黄浦区中山东一路",
        "description": "黄浦江畔的万国建筑博览群，与陆家嘴摩天楼隔江相望。夜幕降临华灯初上时分最为迷人。",
        "opening_hours": "全天开放",
        "popularity_score": 99.2,
    },
    {
        "id": "seed_sh_002", "name": "上海迪士尼乐园", "type": "attraction",
        "city": "上海", "district": "浦东新区",
        "rating": 4.7, "price": 499,
        "tags": ["主题乐园", "亲子", "烟花秀", "热门"],
        "lat": 31.1440, "lng": 121.6580,
        "address": "上海市浦东新区川沙镇黄赵路310号",
        "description": "中国大陆首座迪士尼乐园，拥有全球最高奇幻童话城堡。「点亮奇梦：夜光幻影秀」不可错过。",
        "opening_hours": "08:30-21:30",
        "popularity_score": 97.8,
    },
    {
        "id": "seed_sh_003", "name": "豫园", "type": "attraction",
        "city": "上海", "district": "黄浦区",
        "rating": 4.5, "price": 30,
        "tags": ["江南园林", "历史文化", "城隍庙", "小吃"],
        "lat": 31.2270, "lng": 121.4924,
        "address": "上海市黄浦区福佑路168号",
        "description": "明代私家园林典范，亭台楼阁精巧雅致。毗邻城隍庙美食街，品尝南翔小笼包的好去处。",
        "opening_hours": "08:30-16:30",
        "popularity_score": 86.4,
    },
    {
        "id": "seed_sh_004", "name": "上海外滩W酒店", "type": "hotel",
        "city": "上海", "district": "虹口区",
        "rating": 4.8, "price": 1800,
        "tags": ["奢华", "江景", "网红打卡", "无边泳池"],
        "lat": 31.2460, "lng": 121.4930,
        "address": "上海市虹口区旅顺路66号",
        "description": "坐拥外滩天际线绝美江景，屋顶露天泳池是城中热门打卡地，设计前卫时尚。",
        "opening_hours": "全天候 24h",
        "popularity_score": 93.0,
    },
    {
        "id": "seed_sh_005", "name": "素凯泰酒店(兴业太古汇)", "type": "hotel",
        "city": "上海", "district": "静安区",
        "rating": 4.6, "price": 980,
        "tags": ["设计酒店", "静安寺", "购物便利", "素食餐厅"],
        "lat": 31.2288, "lng": 121.4520,
        "address": "上海市静安区威海路380号",
        "description": "东南亚风格设计酒店，紧邻兴业太古汇与南京西路商圈，闹中取静。",
        "opening_hours": "全天候 24h",
        "popularity_score": 82.1,
    },
    {
        "id": "seed_sh_006", "name": "老吉士(天平路店)", "type": "restaurant",
        "city": "上海", "district": "徐汇区",
        "rating": 4.7, "price": 200,
        "tags": ["本帮菜", "老字号", "红烧肉", "排队"],
        "lat": 31.2035, "lng": 121.4388,
        "address": "上海市徐汇区天平路41号",
        "description": "上海本帮菜标杆，红烧肉、葱烧大乌参、蟹粉豆腐道道经典。店面不大，建议提前预约。",
        "opening_hours": "11:00-14:00 / 17:00-21:00",
        "popularity_score": 87.6,
    },

    # ========== Chengdu ==========
    {
        "id": "seed_cd_001", "name": "成都大熊猫繁育研究基地", "type": "attraction",
        "city": "成都", "district": "成华区",
        "rating": 4.8, "price": 55,
        "tags": ["亲子必去", "国宝熊猫", "自然生态", "拍照"],
        "lat": 30.7310, "lng": 104.1420,
        "address": "成都市成华区熊猫大道1375号",
        "description": "全球最知名的大熊猫保护研究机构，可近距离观赏幼年熊猫活动，建议上午前往熊猫最活跃。",
        "opening_hours": "07:30-18:00",
        "popularity_score": 97.0,
    },
    {
        "id": "seed_cd_002", "name": "宽窄巷子", "type": "attraction",
        "city": "成都", "district": "青羊区",
        "rating": 4.6, "price": 0,
        "tags": ["免费", "历史文化", "成都生活", "茶馆"],
        "lat": 30.6685, "lng": 104.0583,
        "address": "成都市青羊区长顺上街",
        "description": "由宽巷子、窄巷子、井巷子平行排列组成的清代古街，体验成都慢生活与盖碗茶文化。",
        "opening_hours": "全天开放",
        "popularity_score": 94.5,
    },
    {
        "id": "seed_cd_003", "name": "武侯祠", "type": "attraction",
        "city": "成都", "district": "武侯区",
        "rating": 4.5, "price": 50,
        "tags": ["三国文化", "历史古迹", "锦里", "红墙"],
        "lat": 30.6458, "lng": 104.0506,
        "address": "成都市武侯区武侯祠大街231号",
        "description": "纪念诸葛亮与刘备的君臣合祀祠庙，红墙竹影间感受三国风云。旁边的锦里古街汇聚成都小吃。",
        "opening_hours": "08:00-18:30",
        "popularity_score": 89.8,
    },
    {
        "id": "seed_cd_004", "name": "成都博舍酒店", "type": "hotel",
        "city": "成都", "district": "锦江区",
        "rating": 4.8, "price": 1500,
        "tags": ["奢华", "太古里", "设计感", "日式庭院"],
        "lat": 30.6545, "lng": 104.0835,
        "address": "成都市锦江区笔帖式街81号",
        "description": "太古里核心区的奢华设计酒店，融合传统川西院落与现代极简美学，闹中取静的都市隐逸。",
        "opening_hours": "全天候 24h",
        "popularity_score": 91.3,
    },
    {
        "id": "seed_cd_005", "name": "青城山六善酒店", "type": "hotel",
        "city": "成都", "district": "都江堰市",
        "rating": 4.7, "price": 2200,
        "tags": ["度假村", "青城山", "温泉", "避暑"],
        "lat": 30.9025, "lng": 103.5760,
        "address": "成都市都江堰市青城山镇东软大道2号",
        "description": "中国首家六善度假村，坐落在青城山脚下，融入道家文化元素，是远离尘嚣的山居体验。",
        "opening_hours": "全天候 24h",
        "popularity_score": 85.0,
    },
    {
        "id": "seed_cd_006", "name": "小龙坎老火锅(春熙路概念店)", "type": "restaurant",
        "city": "成都", "district": "锦江区",
        "rating": 4.6, "price": 120,
        "tags": ["火锅", "川味", "排队王", "江湖菜"],
        "lat": 30.6555, "lng": 104.0798,
        "address": "成都市锦江区东大街下东大街段2号",
        "description": "成都火锅排队王之一，牛油红锅香辣醇厚，毛肚、鹅肠、黄喉新鲜脆嫩。建议避开饭点高峰。",
        "opening_hours": "11:00-次日02:00",
        "popularity_score": 93.6,
    },

    # ========== Xi'an ==========
    {
        "id": "seed_xa_001", "name": "秦始皇兵马俑博物馆", "type": "attraction",
        "city": "西安", "district": "临潼区",
        "rating": 4.7, "price": 120,
        "tags": ["世界遗产", "世界奇迹", "必打卡", "历史"],
        "lat": 34.3849, "lng": 109.2733,
        "address": "西安市临潼区秦陵北路",
        "description": "世界第八大奇迹，数千个真人大小陶俑阵列展现大秦帝国雄风。建议请讲解员深度体验。",
        "opening_hours": "08:30-17:00",
        "popularity_score": 99.0,
    },
    {
        "id": "seed_xa_002", "name": "西安城墙", "type": "attraction",
        "city": "西安", "district": "碑林区",
        "rating": 4.6, "price": 54,
        "tags": ["骑行", "古城墙", "夜景", "网红"],
        "lat": 34.2585, "lng": 108.9441,
        "address": "西安市碑林区南大街",
        "description": "中国现存规模最大、保存最完整的古代城垣，全长13.7公里。租一辆单车绕城骑行，傍晚的城墙日落美不胜收。",
        "opening_hours": "08:00-22:00",
        "popularity_score": 91.0,
    },
    {
        "id": "seed_xa_003", "name": "回民街", "type": "attraction",
        "city": "西安", "district": "莲湖区",
        "rating": 4.5, "price": 0,
        "tags": ["美食街", "小吃", "夜市", "回民文化"],
        "lat": 34.2690, "lng": 108.9420,
        "address": "西安市莲湖区西大街1号",
        "description": "西安最负盛名的美食街区，羊肉泡馍、肉夹馍、biangbiang面、柿子饼应有尽有。晚上人气最旺。",
        "opening_hours": "各店铺营业时间不一，晚间夜市至22:00",
        "popularity_score": 90.2,
    },
    {
        "id": "seed_xa_004", "name": "西安索菲特传奇酒店", "type": "hotel",
        "city": "西安", "district": "新城区",
        "rating": 4.8, "price": 1300,
        "tags": ["历史建筑", "奢华", "钟楼旁", "法式"],
        "lat": 34.2625, "lng": 108.9485,
        "address": "西安市新城区东新街319号",
        "description": "建于1953年的历史保护建筑，全球仅5家的索菲特传奇之一。法式优雅与古都底蕴交织。",
        "opening_hours": "全天候 24h",
        "popularity_score": 87.0,
    },
    {
        "id": "seed_xa_005", "name": "一间森林青年旅舍", "type": "hotel",
        "city": "西安", "district": "碑林区",
        "rating": 4.3, "price": 80,
        "tags": ["青旅", "背包客", "城墙边", "文艺"],
        "lat": 34.2550, "lng": 108.9400,
        "address": "西安市碑林区顺城南路西段21号",
        "description": "城墙根下的文艺青旅，屋顶露台可远眺城墙。定期举办民谣弹唱与旅行分享会。",
        "opening_hours": "入住 14:00 / 退房 12:00",
        "popularity_score": 72.0,
    },
    {
        "id": "seed_xa_006", "name": "长安大排档(赛格店)", "type": "restaurant",
        "city": "西安", "district": "雁塔区",
        "rating": 4.7, "price": 100,
        "tags": ["陕菜", "网红", "毛笔酥", "葫芦鸡"],
        "lat": 34.2230, "lng": 108.9490,
        "address": "西安市雁塔区小寨东路赛格国际购物中心6层",
        "description": "沉浸式长安主题餐厅，长安葫芦鸡外酥里嫩，毛笔酥创意十足。饭点排队约1小时。",
        "opening_hours": "11:00-21:30",
        "popularity_score": 94.8,
    },

    # ========== Sanya ==========
    {
        "id": "seed_sy_001", "name": "亚龙湾", "type": "attraction",
        "city": "三亚", "district": "吉阳区",
        "rating": 4.8, "price": 0,
        "tags": ["海滩", "免费", "潜水", "度假"],
        "lat": 18.2160, "lng": 109.6400,
        "address": "三亚市吉阳区亚龙湾国家旅游度假区",
        "description": "海南最著名海滩，沙质洁白细软，海水清澈见底。「天下第一湾」名不虚传，各类水上运动丰富。",
        "opening_hours": "全天开放",
        "popularity_score": 97.5,
    },
    {
        "id": "seed_sy_002", "name": "天涯海角", "type": "attraction",
        "city": "三亚", "district": "天涯区",
        "rating": 4.4, "price": 81,
        "tags": ["爱情圣地", "海边奇石", "日落", "天涯"],
        "lat": 18.2280, "lng": 109.3920,
        "address": "三亚市天涯区天涯镇",
        "description": "以「天涯」「海角」巨石闻名的风景名胜区。碧海蓝天、椰林树影，是情侣与新人婚纱照圣地。",
        "opening_hours": "07:30-18:00",
        "popularity_score": 88.4,
    },
    {
        "id": "seed_sy_003", "name": "蜈支洲岛", "type": "attraction",
        "city": "三亚", "district": "海棠区",
        "rating": 4.7, "price": 144,
        "tags": ["潜水天堂", "海岛", "水上项目", "玻璃海"],
        "lat": 18.2660, "lng": 109.7650,
        "address": "三亚市海棠区蜈支洲岛",
        "description": "被誉为「中国马尔代夫」，海水能见度可达27米，是海南最佳潜水地之一。摩托艇、拖伞等水上项目丰富。",
        "opening_hours": "08:00-17:30(末班船17:30离岛)",
        "popularity_score": 95.0,
    },
    {
        "id": "seed_sy_004", "name": "三亚亚特兰蒂斯酒店", "type": "hotel",
        "city": "三亚", "district": "海棠区",
        "rating": 4.9, "price": 2500,
        "tags": ["奢华度假", "水世界", "海底套房", "亲子"],
        "lat": 18.2820, "lng": 109.7520,
        "address": "三亚市海棠区海棠北路36号",
        "description": "七星级综合度假区，拥有失落的空间水族馆与水世界乐园。海底套房可透过落地窗看海洋生物游弋。",
        "opening_hours": "全天候 24h",
        "popularity_score": 98.0,
    },
    {
        "id": "seed_sy_005", "name": "三亚太阳湾柏悦酒店", "type": "hotel",
        "city": "三亚", "district": "吉阳区",
        "rating": 4.8, "price": 2000,
        "tags": ["私密海滩", "奢华", "海景", "设计"],
        "lat": 18.2060, "lng": 109.6290,
        "address": "三亚市吉阳区亚龙湾国家旅游度假区太阳湾路5号",
        "description": "独占太阳湾一隅的私密奢华酒店，拥有独立沙滩与艺术收藏品。是追求安静度假的首选。",
        "opening_hours": "全天候 24h",
        "popularity_score": 90.5,
    },
    {
        "id": "seed_sy_006", "name": "第一市场海鲜加工", "type": "restaurant",
        "city": "三亚", "district": "天涯区",
        "rating": 4.5, "price": 150,
        "tags": ["海鲜", "现捞现做", "夜市", "本地味"],
        "lat": 18.2420, "lng": 109.5120,
        "address": "三亚市天涯区新建街155号",
        "description": "三亚最地道的海鲜体验：自己在一楼市场选海鲜，楼上加工坊现做。推荐椒盐皮皮虾和香辣蟹。",
        "opening_hours": "06:00-21:00",
        "popularity_score": 86.0,
    },

    # ========== Hangzhou ==========
    {
        "id": "seed_hz_001", "name": "西湖", "type": "attraction",
        "city": "杭州", "district": "西湖区",
        "rating": 4.9, "price": 0,
        "tags": ["免费", "世界遗产", "泛舟", "十景"],
        "lat": 30.2437, "lng": 120.1462,
        "address": "杭州市西湖区龙井路1号",
        "description": "杭州的灵魂，世界文化遗产。断桥残雪、苏堤春晓、雷峰夕照——西湖十景名不虚传。泛舟湖上最为惬意。",
        "opening_hours": "全天开放",
        "popularity_score": 99.5,
    },
    {
        "id": "seed_hz_002", "name": "灵隐寺", "type": "attraction",
        "city": "杭州", "district": "西湖区",
        "rating": 4.7, "price": 75,
        "tags": ["佛教圣地", "千年古刹", "济公", "飞来峰"],
        "lat": 30.2433, "lng": 120.0968,
        "address": "杭州市西湖区法云弄1号",
        "description": "中国十大名刹之一，始建于东晋。飞来峰摩崖石刻精美绝伦。每年除夕敲钟祈福是杭州人传统。",
        "opening_hours": "07:00-18:00",
        "popularity_score": 93.6,
    },
    {
        "id": "seed_hz_003", "name": "龙井村", "type": "attraction",
        "city": "杭州", "district": "西湖区",
        "rating": 4.5, "price": 0,
        "tags": ["茶文化", "茶园", "徒步", "小众"],
        "lat": 30.2250, "lng": 120.1130,
        "address": "杭州市西湖区龙井路龙井村",
        "description": "西湖龙井茶核心产区，春季采茶时节最值得造访。从九溪烟树沿山路徒步至龙井村，一路茶园叠翠。",
        "opening_hours": "全天开放(部分茶庄营业至17:00)",
        "popularity_score": 78.5,
    },
    {
        "id": "seed_hz_004", "name": "杭州法云安缦", "type": "hotel",
        "city": "杭州", "district": "西湖区",
        "rating": 4.9, "price": 5000,
        "tags": ["顶奢", "禅意", "灵隐旁", "隐世"],
        "lat": 30.2420, "lng": 120.0980,
        "address": "杭州市西湖区法云弄22号",
        "description": "由古村落改造的奢华隐世酒店，毗邻灵隐寺。黄土墙、竹篱笆，以极简禅意诠释江南山居。",
        "opening_hours": "全天候 24h",
        "popularity_score": 95.0,
    },
    {
        "id": "seed_hz_005", "name": "西溪悦榕庄", "type": "hotel",
        "city": "杭州", "district": "西湖区",
        "rating": 4.7, "price": 1800,
        "tags": ["度假村", "湿地", "江南水乡", "SPA"],
        "lat": 30.2710, "lng": 120.0600,
        "address": "杭州市西湖区紫金港路西溪天堂国际旅游综合体2号",
        "description": "坐落在西溪湿地内的江南水乡风格度假村，独立庭院别墅、泛舟河道入住，独享湿地静谧。",
        "opening_hours": "全天候 24h",
        "popularity_score": 88.2,
    },
    {
        "id": "seed_hz_006", "name": "杭州酒家(延安路店)", "type": "restaurant",
        "city": "杭州", "district": "上城区",
        "rating": 4.6, "price": 120,
        "tags": ["杭帮菜", "老字号", "西湖醋鱼", "叫花鸡"],
        "lat": 30.2490, "lng": 120.1670,
        "address": "杭州市上城区延安路205号",
        "description": "百年老字号杭帮菜馆，西湖醋鱼、龙井虾仁、叫花鸡是招牌。性价比高，本地人也常光顾。",
        "opening_hours": "11:00-14:00 / 17:00-20:30",
        "popularity_score": 89.5,
    },
]


def search_poi(
    keyword: str = "",
    city: str = "",
    poi_type: str = "",
    page: int = 1,
    page_size: int = 10,
) -> dict:
    """Search POI from seed data (simulating ES search).

    Supports keyword matching, city filter, type filter, popularity sort, pagination.
    """
    results = list(_SEED_POIS)

    # Keyword filter
    if keyword:
        kw = keyword.lower()
        results = [
            p for p in results
            if kw in p["name"].lower()
            or kw in p.get("description", "").lower()
            or any(kw in t.lower() for t in p.get("tags", []))
            or kw in p.get("city", "").lower()
            or kw in p.get("address", "").lower()
        ]

    # City filter
    if city:
        results = [p for p in results if p.get("city") == city]

    # Type filter
    if poi_type:
        results = [p for p in results if p.get("type") == poi_type]

    # Sort by popularity score descending
    results.sort(key=lambda x: x.get("popularity_score", 0), reverse=True)

    total = len(results)

    # Paginate
    start = (page - 1) * page_size
    end = start + page_size
    items = results[start:end]

    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
    }


def suggest(keyword: str, size: int = 5) -> list:
    """Suggest POI names from seed data (name + city matching)."""
    if not keyword:
        return []
    kw = keyword.lower()
    # Name match first (higher priority), then city match
    name_matches = [p["name"] for p in _SEED_POIS if kw in p["name"].lower()]
    city_matches = [p["name"] for p in _SEED_POIS
                    if kw in p.get("city", "").lower() and p["name"] not in name_matches]
    all_matches = name_matches + city_matches
    # Deduplicate
    seen = set()
    unique = []
    for m in all_matches:
        if m not in seen:
            seen.add(m)
            unique.append(m)
    return unique[:size]
