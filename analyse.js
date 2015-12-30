var plan = require('./reference/plancomptable');
var fs = require('fs');
var async = require('async');
var csv = require('csv-parser');
var q = require('q');

var tab = [70311,7067,7083,70878,73111,7321,7351,7411,74121,74127,742,7473,7482,74832,74833,74834,74835,752,758,761,7718,775];
var tab2 = [60611,60612,60621,60622,60631,60632,60633,60636,6064,6067,6068,611,6122,61521,61522,61523,61524,
	61551,61558,6156,616,6182,6188,6225,6226,6232,6257,6261,6262,6281,62878,6288,6332,6336,6338,63512,6411,6413,
	6419,6451,6453,6454,6455,6456,6458,6475,6531,6533,6535,6541,6553,6554,657361,657362,6574,66111,675,6811
];

for (var i = 0; i < tab2.length ; i++) {
	console.log(plan[tab2[i]]); // '['+tab2[i]+'] '+
}

function readDoc (pathToDoc) {
	var deferred = q.defer();

	var tab = [];

	fs.createReadStream(pathToDoc)
		.pipe(csv({
			raw: false,     // do not decode to utf-8 strings
			separator: ';'
		}))
		.on('data', function(data) {
			tab.push({
				NCompte: data.NCompte,
				BEntreeD: data.BEntreeD,
				BEntreeC: data.BEntreeC,
				OBDNA: data.OBDNA,
				OBCNA: data.OBCNA,
				ONBD: data.ONBD,
				ONBC: data.ONBC,
				OOBD: data.OOBD,
				OOBC: data.OOBC,
				SoldeD: data.SoldeD,
				SoldeC: data.SoldeC
			});
		})
		.on('error', function (err){
			deferred.reject(err);
		})
		.on('end', function (){
			deferred.resolve(tab);
		});

	return deferred.promise
}

function bilanSimple (array) {

	var deferred = q.defer();

	var charges = 0;
	var recettes = 0;

	var keys = array[12];

	async.each(array, function (ligne, next){
		switch (ligne.NCompte[0]) {
			case '6':
				charges = charges + Number(ligne.SoldeD.replace(',','.'));
				next();
				break;
			case '7':
				recettes = recettes + Number(ligne.SoldeC.replace(',','.'));
				next();
				break;
			default :
				next();
				break;
		}
	}, function (err) {
		if (err) {
			deferred.reject(err);
		}
		else {
			deferred.resolve(recettes - charges);
		}
	});

	return deferred.promise;


}

readDoc('./data/meaux.csv')
	.then(function(array){
		return bilanSimple(array)
	})
	.then(function(resultat){
		console.log(resultat);
	})
	.catch(function (err) {
		console.log('Something wrong happened :'+err)
	});