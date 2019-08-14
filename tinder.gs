sheetId = "スプレッドシートのID";
folderId = "DriveのフォルダのID";


//スワイプしたプロフィールの情報を記録する
function doPost(e) {
  var sheet = SpreadsheetApp.openById(sheetId).getSheets()[0];//スプレッドシートにアクセス
  var id = e.parameter.id;
  var name = e.parameter.name;
  var age = e.parameter.age;
  var gender = e.parameter.gender;
  var distance_mi = e.parameter.distance_mi;
  var bio = e.parameter.bio;
  var jobs = e.parameter.jobs;
  var schools = e.parameter.schools;
  var match = 0;
  var timestamp = Math.round((new Date()).getTime() / 1000);
  var datas = [
    [id, name, age, gender, distance_mi, bio, jobs, schools, match, timestamp]
  ]
  var photo0 = e.parameter.photo0;
  var photo1 = e.parameter.photo1;
  var photo2 = e.parameter.photo2;
  var photo3 = e.parameter.photo3;
  var photo4 = e.parameter.photo4;
  var photo5 = e.parameter.photo5;
  
  var photos = [photo0, photo1, photo2, photo3, photo4, photo5];
  
  var row = sheet.getLastRow() + 1;//最終行を取得
  sheet.getRange(row, 1, 1, 10).setValues(datas);
  
  //写真を保存
  for(i=0;i<photos.length;i++){
    var photo = photos[i];
    if (photo != null) {
      var name = id + "-" + i + ".jpg";
      var blob = getImage(photo, name);
      saveFile(blob);
    }
  }
}


function getImage(url, name) {
  var response = UrlFetchApp.fetch(url);//urlにアクセスしてデータを取得
  var response = response.getBlob().getAs("image/jpeg").setName(name);//
  return response
}

function getVideo(url, name) {
  var response = UrlFetchApp.fetch(url);
  var response = response.getBlob().getAs("application/octet-stream").setName(name);
  return response
}

function saveFile(blob) {
  var folder = DriveApp.getFolderById(folderId);
  folder.createFile(blob)
}

//マッチしたプロフィールの情報を記録する
function doGet(e){
  var sheet = SpreadsheetApp.openById(sheetId).getSheets()[0];
  var id = e.parameter.id;
  
  var ids=sheet.getRange(1,1,row).getValues();//これまでマッチした人すべてのidを取得
  for(i=0;i<ids.length;i++){
    if(id==ids[i][0]){
      sheet.getRange(i+1,9).setValue(1);
      return;
    }
  }
}