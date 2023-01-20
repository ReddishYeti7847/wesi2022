// Initialize and add the map
function initMap() {
  // 座標
    var str;
    var lat;
    var center_lat = 0;
    var lng;
    var center_lng = 0;
    var zoom;
    var count = document.getElementById("marker_count").value;

    //地図の拡大倍率
    if (count == 1) {
        zoom = 15;
    } else {
        zoom = 8;
    }

    //中心位置を求める
    for (var i = 0; i < count; i++) {
        str = "lat" + i.toString();
        lat = document.getElementById(str).value;
        str = "lng" + i.toString();
        lng = document.getElementById(str).value;

        center_lat = center_lat + parseFloat(lat);
        center_lng = center_lng + parseFloat(lng);
    }
    console.log("?");


    center_lat = center_lat / count;
    center_lng = center_lng / count;

    var options = {
        zoom: zoom,
        center: new google.maps.LatLng(center_lat, center_lng),
        mapTypeId: 'roadmap',
        disableDefaultUI: true,
        zoomControl: true,
        mapTypeControl: true,
		mapTypeControlOptions: {
  		    style: google.maps.MapTypeControlStyle.DROPDOWN_MENU,
  		    position: google.maps.ControlPosition.LEFT_TOP
		}
    }
    var map = new google.maps.Map(document.getElementById("map"), options);
    for (var i = 0; i < count; i++) {
        str = "lat" + i.toString();
        lat = document.getElementById(str).value;
        str = "lng" + i.toString();
        lng = document.getElementById(str).value;
        
        var marker = new google.maps.Marker({ //マーカー
            position: new google.maps.LatLng(lat, lng),
            map: map
        });
    }

    console.log(center_lat, center_lng, count);
    console.log(position);
}

window.initMap = initMap;


/*
    var position = new google.maps.LatLng(<%= @site.latitude %>, <%= @site.longitude %>);
    var options = {
      zoom: 15,
      center: position, 
      mapTypeId: 'roadmap',
      disableDefaultUI: true,
      zoomControl: true,
      mapTypeControl: true,
		  mapTypeControlOptions: {
  			style: google.maps.MapTypeControlStyle.DROPDOWN_MENU,
  			position: google.maps.ControlPosition.LEFT_TOP
		  }
    };
    var map = new google.maps.Map(document.getElementById('map'), options);
    var marker = new google.maps.Marker({
      position: position,
      map: map
    });
*/