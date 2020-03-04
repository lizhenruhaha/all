// pages/myslef/myself.js

var app = getApp()
//导包
const cookieUtil=require('../../utils/util.js')

Page({

  /**
   * 页面的初始数据
   */
  data: {
     
  },
  
  getcookie:function(){
    wx.request({
      //向Django端发起请求
      url: 'http://127.0.0.1:8000/app/testcookie',
      success:function(res){
        //通过导包获取util里面的方法获取cookie
        // Django中的session中间键也要打开
        var cookie = cookieUtil.getSessionIDFromResponse(res)
        console.log(cookie)
        //将获取的cookie保存到本地
        cookieUtil.setCookieToStorage(cookie)
      }
    })
  },
  sendcookie:function(){
    var newcookie=cookieUtil.getCookieFromStorage()
    var header={}
    header.Cookie=newcookie
    wx.request({
      url: 'http://127.0.0.1:8000/app/getcookie',
      header:header,
      success:function(res){
        console.log('成功')
        console.log(res.data)
      }
    })
  },
  authorize:function(){
    wx.login({
        success:function(res){
          //携带一些数据,用post
          //获取用户登录昵称
          var nickname=app.globalData.userInfo.nickName
          wx.request({
            url: 'http://127.0.0.1:8000/app/authorize',
            method:'POST',
            data:{
              code:res.code,
              nickname:nickname
            },
            success:function(res){
              wx.showToast({
                title: '认证成功',
              })
              //获取返回来的session
              var cookie=cookieUtil.getSessionIDFromResponse(res)
              console.log(cookie)
              cookieUtil.setCookieToStorage(cookie)
            }
          })
        }
    })
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {

  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  }
})