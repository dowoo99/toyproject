function countryName() {
  
      let country = $('#country').val()
      let url = 'https://apis.data.go.kr/1262000/TravelAlarmService2/getTravelAlarmList2?serviceKey=hS9Bs6Nf3h3YN8UoMNUNdJBiAs0Ub3smX3bnv85MNTgqCnCeFL0NGg%2F0Vs%2BSL7pHZpugBzpRzpcN5yKXJGivOg%3D%3D&returnType=JSON&numOfRows=10&cond[country_nm::EQ]='+ country +'&pageNo=1'
      $.ajax({
          type: "GET",
          url: url,
          data: {},
          success: function (response) {
              let rows = response.data
              for (let i = 0; i < rows.length; i++) {
                  let desc = rows[i].remark
                  let country = rows[i].country_nm
                  let day = rows[i].written_dt
                  let level = rows[i].alarm_lvl
                  let flag = rows[i].flag_download_url
                  
                  let temp_html =` <div class="swiper-slide">
                                   <div class="swiper-zoom-container">
                                    <img class="flag" src="${flag}" />
                                </div>
                                <h2 class="country">${country}</h2>
                                <p class="desc">${desc}</p>
                                <p class="day">${day}</p>
                                </div>`

                                $('.swiper-wrapper').append(temp_html);

              }
          }
      })
  
}