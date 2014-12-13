/**
 * Created by JerryPark on 2014-12-13.
 */
$(window).load(function(){
    var myDate = new Date();
    $("#p_top_date").text(myDate.getFullYear()+"년 "+(myDate.getMonth()+1)+"월 "+myDate.getDay()+"일");
});