
DROP TABLE IF EXISTS clientInfo;
CREATE TABLE clientInfo(
    oid INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    fengId TEXT,
    appleid TEXT NOT NULL,
    pwd TEXT NOT NULL,
    govidType TEXT NOT NULL,
    govid TEXT NOT NULL,
    area TEXT NOT NULL,
    models TEXT NOT NULL,
    quantity INTEGER DEFAULT 1,
    isActive INTEGER DEFAULT 1
);

DROP TABLE IF EXISTS store;
CREATE TABLE store(
    oid INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    storeId TEXT NOT NULL,
    storeName TEXT NOT NULL,
    areaName TEXT NOT NULL,
    area TEXT NOT NULL
);


INSERT INTO store (storeId, storeName, areaName, area) VALUES ("R359","南京东路","上海","shanghai");
INSERT INTO store (storeId, storeName, areaName, area) VALUES ("R389","浦东","上海","shanghai");
INSERT INTO store (storeId, storeName, areaName, area) VALUES ("R390","香港广场","上海","shanghai");
INSERT INTO store (storeId, storeName, areaName, area) VALUES ("R401","上海环贸 iapm","上海","shanghai");
insert into store (storeid, storename, areaname, area) values ("R581","五角场","上海","shanghai");
insert into store (storeid, storename, areaname, area) values ("R683","环球港","上海","shanghai");
insert into store (storeid, storename, areaname, area) values ("R320","三里屯","北京","beijing");
insert into store (storeid, storename, areaname, area) values ("R388","西单大悦城","北京","beijing");
insert into store (storeid, storename, areaname, area) values ("R448","王府井","北京","beijing");
insert into store (storeid, storename, areaname, area) values ("R479","华贸购物中心","北京","beijing");
insert into store (storeid, storename, areaname, area) values ("R645","朝阳大悦城","北京","beijing");
insert into store (storeid, storename, areaname, area) values ("R493","南京艾尚天地","南京","nanjing");
insert into store (storeid, storename, areaname, area) values ("R643","虹悦城","南京","nanjing");
insert into store (storeid, storename, areaname, area) values ("R571","南宁万象城","南宁","nanning");
insert into store (storeid, storename, areaname, area) values ("R644","厦门新生活广场","厦门","xiamen");
insert into store (storeid, storename, areaname, area) values ("R478","百年城","大连","dalian");
insert into store (storeid, storename, areaname, area) values ("R609","大连恒隆广场","大连","dalian");
insert into store (storeid, storename, areaname, area) values ("R579","天津恒隆广场","天津","tianjin");
insert into store (storeid, storename, areaname, area) values ("R637","天津大悦城","天津","tianjin");
insert into store (storeid, storename, areaname, area) values ("R638","银河国际购物中心","天津","tianjin");
insert into store (storeid, storename, areaname, area) values ("R577","天环广场","广州","guangzhou");
insert into store (storeid, storename, areaname, area) values ("R502","成都万象城","成都","chengdu");
insert into store (storeid, storename, areaname, area) values ("R580","成都太古里","成都","chengdu");
insert into store (storeid, storename, areaname, area) values ("R574","无锡恒隆广场","无锡","wuxi");
insert into store (storeid, storename, areaname, area) values ("R471","西湖","杭州","hangzhou");
insert into store (storeid, storename, areaname, area) values ("R532","杭州万象城","杭州","hangzhou");
insert into store (storeid, storename, areaname, area) values ("R534","中街大悦城","沈阳","shenyang");
insert into store (storeid, storename, areaname, area) values ("R576","沈阳万象城","沈阳","shenyang");
insert into store (storeid, storename, areaname, area) values ("R648","济南恒隆广场","济南","jinan");
insert into store (storeid, storename, areaname, area) values ("R484","深圳益田假日广场","深圳","shenzhen");
insert into store (storeid, storename, areaname, area) values ("R646","泰禾广场","福州","fuzhou");
insert into store (storeid, storename, areaname, area) values ("R572","郑州万象城","郑州","zhengzhou");
insert into store (storeid, storename, areaname, area) values ("R476","重庆北城天街","重庆","chongqing");
insert into store (storeid, storename, areaname, area) values ("R480","解放碑","重庆","chongqing");
insert into store (storeid, storename, areaname, area) values ("R573","重庆万象城","重庆","chongqing");
insert into store (storeid, storename, areaname, area) values ("R557","青岛万象城","青岛","qingdao");
INSERT INTO store (storeId, storeName, areaName, area) VALUES ("R673", "apm Hong Kong", "香港", "HongKong");
INSERT INTO store (storeId, storeName, areaName, area) VALUES ("R499", "Canton Road", "香港", "HongKong");
INSERT INTO store (storeId, storeName, areaName, area) VALUES ("R409", "Causeway Bay", "香港", "HongKong");
INSERT INTO store (storeId, storeName, areaName, area) VALUES ("R485", "Festival Walk", "香港", "HongKong");
INSERT INTO store (storeId, storeName, areaName, area) VALUES ("R428", "ifc mall", "香港", "HongKong");
INSERT INTO store (storeId, storeName, areaName, area) VALUES ("R610", "New Town Plaza", "香港", "HongKong");


drop table if exists model;
create table model(
    oid integer primary key autoincrement not null,
    modelid text not null,
    modelname text not null
);

insert into model (modelid, modelname) values ("MNH22CH/A", "iphone 7 jet black - 128 GB");
INSERT INTO model (modelId, modelName) VALUES ("MNH72CH/A", "iPhone 7 Jet Black - 256 GB");
INSERT INTO model (modelId, modelName) VALUES ("MNGQ2CH/A", "iPhone 7 Black - 32 GB");
INSERT INTO model (modelId, modelName) VALUES ("MNGX2CH/A", "iPhone 7 Black - 128 GB");
INSERT INTO model (modelId, modelName) VALUES ("MNH32CH/A", "iPhone 7 Black - 256 GB");
INSERT INTO model (modelId, modelName) VALUES ("MNGT2CH/A", "iPhone 7 Gold - 32 GB");
INSERT INTO model (modelId, modelName) VALUES ("MNH02CH/A", "iPhone 7 Gold - 128 GB");
INSERT INTO model (modelId, modelName) VALUES ("MNH52CH/A", "iPhone 7 Gold - 256 GB");
INSERT INTO model (modelId, modelName) VALUES ("MNGW2CH/A", "iPhone 7 Rose Gold - 32 GB");
INSERT INTO model (modelId, modelName) VALUES ("MNH12CH/A", "iPhone 7 Rose Gold - 128 GB");
INSERT INTO model (modelId, modelName) VALUES ("MNH62CH/A", "iPhone 7 Rose Gold - 256 GB");
INSERT INTO model (modelId, modelName) VALUES ("MNGR2CH/A", "iPhone 7 Silver - 32 GB");
INSERT INTO model (modelId, modelName) VALUES ("MNGY2CH/A", "iPhone 7 Silver - 128 GB");
INSERT INTO model (modelId, modelName) VALUES ("MNH42CH/A", "iPhone 7 Silver - 256 GB");
INSERT INTO model (modelId, modelName) VALUES ("MNFU2CH/A", "iPhone 7 Plus Jet Black - 128 GB");
INSERT INTO model (modelId, modelName) VALUES ("MNG02CH/A", "iPhone 7 Plus Jet Black - 256 GB");
INSERT INTO model (modelId, modelName) VALUES ("MNRJ2CH/A", "iPhone 7 Plus Black - 32 GB");
INSERT INTO model (modelId, modelName) VALUES ("MNFP2CH/A", "iPhone 7 Plus Black - 128 GB");
INSERT INTO model (modelId, modelName) VALUES ("MNFV2CH/A", "iPhone 7 Plus Black - 256 GB");
INSERT INTO model (modelId, modelName) VALUES ("MNRM2CH/A", "iPhone 7 Plus Rose Gold - 32 GB");
INSERT INTO model (modelId, modelName) VALUES ("MNFT2CH/A", "iPhone 7 Plus Rose Gold- 128 GB");
INSERT INTO model (modelId, modelName) VALUES ("MNFY2CH/A", "iPhone 7 Plus Rose Gold - 256 GB");
INSERT INTO model (modelId, modelName) VALUES ("MNRL2CH/A", "iPhone 7 Plus Gold - 32 GB");
INSERT INTO model (modelId, modelName) VALUES ("MNFR2CH/A", "iPhone 7 Plus Gold - 128 GB");
INSERT INTO model (modelId, modelName) VALUES ("MNFX2CH/A", "iPhone 7 Plus Gold - 256 GB");
INSERT INTO model (modelId, modelName) VALUES ("MNRK2CH/A", "iPhone 7 Plus Silver - 32 GB");
INSERT INTO model (modelId, modelName) VALUES ("MNFQ2CH/A", "iPhone 7 Plus Silver - 128 GB");
INSERT INTO model (modelId, modelName) VALUES ("MNFW2CH/A", "iPhone 7 Plus Silver - 256 GB");


DROP TABLE IF EXISTS applog;
CREATE TABLE applog(
    oid INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    area TEXT,
    storeName TEXT,
    modelName TEXT,
    appleId TEXT,
    fengId TEXT,
    sleepTime TEXT,
    totalTime TEXT,
    error TEXT,
    timestamp INTEGER NOT NULL
);

DROP TABLE IF EXISTS cellphoneInfo;
CREATE TABLE cellphoneInfo(
    oid INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    phoneNumber TEXT,
    todayCount INTEGER,
    availCount INTEGER,
    timestamp TEXT
);
INSERT INTO cellphoneInfo (phoneNumber, todayCount, availCount, timestamp) VALUES ("18310503261", 0, 0, datetime(current_timestamp, 'localtime'));
INSERT INTO cellphoneInfo (phoneNumber, todayCount, availCount, timestamp) VALUES ("18310729604", 0, 0, datetime(current_timestamp, 'localtime'));

DROP TABLE IF EXISTS rcode;
CREATE TABLE rcode(
    oid INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    rcode TEXT,
    appleId TEXT,
    phoneNumber TEXT,
    timestamp TEXT NOT NULL
);
