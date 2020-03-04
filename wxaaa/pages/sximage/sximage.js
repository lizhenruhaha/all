Page({
  data: {
    // 待上传的图片, 本地地址
    files: [],
    //下载的文件列表
    downloadedBackupedFiles:[]

  },
  chooseImage: function (e) {
    var that = this;
    wx.chooseImage({
      sizeType: ['original', 'compressed'], // 可以指定是原图还是压缩图，默认二者都有
      sourceType: ['album', 'camera'], // 可以指定来源是相册还是相机，默认二者都有
      success: function (res) {
        // 返回选定照片的本地文件路径列表，tempFilePath可以作为img标签的src属性显示图片
        that.setData({
          files: that.data.files.concat(res.tempFilePaths)
        });
      }
    })
  },
  previewImage: function (e) {
    wx.previewImage({
      current: e.currentTarget.id, // 当前显示图片的http链接
      urls: this.data.files // 需要预览的图片http链接列表
    })
  },
  // 上传图片文件
  uploadpic: function () {
    for (var i = 0; i < this.data.files.length; i++) {
      var filePath = this.data.files[i]
      wx.uploadFile({
        url: 'http://127.0.0.1:8000/app/down',
        filePath: filePath,
        name: 'test'+filePath,
        success: function (res) {
          console.log(res.data),
            console.log(typeof (res.data))
        }
      })
    }
  },
  // 下载图片
  loadpic: function (imgItem) {
    var that = this
    wx.downloadFile({
      url: 'http://127.0.0.1:8000/app/down',
      success: function (res) {
        console.log('成功了..')
        console.log(res.tempFilePath)
        console.log(res.filePath)
        var tmpPath = res.tempFilePath
        var newDownloadedBackupedFiles = that.data.downloadedBackupedFiles
        newDownloadedBackupedFiles.push(tmpPath)
        that.setData({
          downloadedBackupedFiles: newDownloadedBackupedFiles
        })
      }
    })
  },

  // 删除后台图片
  deletepic: function (imgItem) {
    wx.request({
      url: 'http://127.0.0.1:8000/app/down?name=ac9c.png',
      method: 'DELETE',
      success: function (res) {
        // 后台反馈给前端的数据
        console.log(res.data)
        wx.showToast({
          title: res.data,
        })
      }
    })
  },

  // 长按确认删除函数
  longTapConfirm: function (e) {
    var that = this
    var confirmList = ["删除这个图片","其它"]
    wx.showActionSheet({
      itemList: confirmList,
      success: function (res) {
        // 这个就是点击了取消按钮
        //res.tapindex 来判断condirmList具体是哪一个
        if (res.tapIndex==0) {
          var imageIndex = e.currentTarget.dataset.index
          var imageItem = that.data.downloadedBackupedFiles[imageIndex]
          var newList = that.data.downloadedBackupedFiles
          newList.splice(imageIndex, 1)
          that.setData({
            downloadedBackupedFiles: newList
          })
          that.deletepic(imageItem)
          }else{
            console.log(confirmList[res.tapIndex])
          }
      }
    })
  },
});