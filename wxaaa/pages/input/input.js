// pages/a/a.js
var app=getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    qq:'',
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
   
  },

  qq:function(e){
    this.data.qq=e.detail.value
  },
  showTop:function(){
    var qqname = this.data.qq
    wx:wx.request({
      url: 'http://japi.juhe.cn/qqevaluate/qq?key=d0f580a311243e3d3452acf6482fbff5&qq='+qqname,
      success: function(res) {
        var finall = res.data.result.data.conclusion + res.data.result.data.analysis
        console.log(finall)
        app.globalData.result=finall
        console.log(app.globalData.result)
        wx.navigateTo({
          url: '../b/b',
        })
      },
      fail: function(res) {
        console.log(res.errMsg)
      },
    })
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