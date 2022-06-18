function countryName() {
  let country = $("#country").val();

  $(".header").empty();
  $.ajax({
    type: "GET",
    url: "https://apis.data.go.kr/1262000/TravelAlarmService2/getTravelAlarmList2?serviceKey=hS9Bs6Nf3h3YN8UoMNUNdJBiAs0Ub3smX3bnv85MNTgqCnCeFL0NGg%2F0Vs%2BSL7pHZpugBzpRzpcN5yKXJGivOg%3D%3D&returnType=JSON&numOfRows=10&cond[country_nm::EQ]=" +
      country +
      "&pageNo=1",
    data: {},
    success: function (response) {
      let rows = response.data;
      for (let i = 0; i < rows.length; i++) {
        let desc = rows[i].remark;
        let country = rows[i].country_nm;
        let day = rows[i].written_dt;
        let level = rows[i].alarm_lvl;
        let flag = rows[i].flag_download_url;

        let temp_html_1 = ` <h1>${country}</h1>
        <img src="${flag}" alt="flag">`;
        $(".header").append(temp_html_1);
      }
    },
  });

  $(".body").empty();
  $.ajax({
    type: "GET",
    url:
      "https://apis.data.go.kr/1262000/CountryHistoryService2/getCountryHistoryList2?serviceKey=aUnV4FRi29Fgy9J2UIetwPVSzHaN5HoVt1EzG8urQTfK6lskwIFLAGDs799RBLopbV%2BgtZfsOcfyxsE9FdYYLg%3D%3D&returnType=JSON&numOfRows=1&cond[country_nm::EQ]=%EA%B0%80%EB%82%98&" +
      country +
      "cond[country_iso_alp2::EQ]=GH&pageNo=1",
    data: {},
    success: function (response2) {
      let rows = response2.data;
      for (let i = 0; i < rows.length; i++) {
        let title = rows[i]["title"];
        let desc = rows[i]["txt_origin_cn"];
        let wrt_dt = rows[i]["wrt_dt"];

        console.log(rows)

        let temp_html = `<li>
                              <h3 id="title">${title}</h3>
                              <p id="wrt_dt">${wrt_dt}</p>
                              <p id="txt_origin">${desc}</p>
                        </li>`;
        $(".body").append(temp_html);
      }
    },
  });

  $.ajax({
    type: "GET",
    url: "https://apis.data.go.kr/1262000/LocalContactService2/getLocalContactList2?serviceKey=hS9Bs6Nf3h3YN8UoMNUNdJBiAs0Ub3smX3bnv85MNTgqCnCeFL0NGg%2F0Vs%2BSL7pHZpugBzpRzpcN5yKXJGivOg%3D%3D&returnType=JSON&numOfRows=10&cond[country_nm::EQ]=" + country + "&pageNo=1",
    data: {},
    success: function (response3) {
      let rows = response3.data;
      for (let i = 0; i < rows.length; i++) {
        let remark = rows[i].contact_remark;
        let temp_html = `${remark}`

        $('.infoArea').append(temp_html)
      }

    }
  });
}



