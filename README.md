## 实践与总结

爬虫的过程简单的说就是把网页的内容下载到本地，很多时候是html文件，html中的内容可以处理为树形结构，使用bs4等库能够很方便定位目标内容，并做相应的处理。

### 爬虫方式搭配

#### 正则表达式

如果所需的内容集中在一个页面且内容不多，则直接通过复制网页源码再通过VScode的正则表达处理便能快速的提取出目标内容。（如果是处于json中的数据也同样用正则表达来提取）

这种方式很原始，但也简单有效，甚至快捷。

#### request、bs4、selenium

如果目标内容有规律的分布在多个网页中，则可以通过selenium使用浏览器打开网页，再提取其中的内容（[例如获取微信文章列表.py](https://gitee.com/team317/web-crawler/blob/master/%E8%8E%B7%E5%8F%96%E5%BE%AE%E4%BF%A1%E6%96%87%E7%AB%A0%E5%88%97%E8%A1%A8.py)）

也可以使用requests库和bs4库来完成提取，这种方式的缺点是要手动设置代理、cookies等信息，更麻烦一些，而selenium则无需手动设置代理、cookies（使用selenium时也可以添加cookies，见[简书使用selenium添加cookie完成登录](https://gitee.com/team317/web-crawler/blob/master/%E7%AE%80%E4%B9%A6%E4%BD%BF%E7%94%A8selenium%E6%B7%BB%E5%8A%A0cookie%E5%AE%8C%E6%88%90%E7%99%BB%E5%BD%95.py)）



### 踩坑记录

#### ip被封

在[获取微信文章列表.py](https://gitee.com/team317/web-crawler/blob/master/%E8%8E%B7%E5%8F%96%E5%BE%AE%E4%BF%A1%E6%96%87%E7%AB%A0%E5%88%97%E8%A1%A8.py)实践中，由于内容分布在不同的网页，所以写了循环来处理，但忘了sleep，使得访问过于频繁，最后似乎ip被封，无法继续访问。网站可以通过ip每秒的访问频率来决定是否封ip，频繁的爬虫会增加网站的负担，这是反爬虫的理由之一。在爬虫时，应将频率控制在正常用户的访问频率限度内，例如4到10秒访问一次。在循环访问的代码中，需设置sleep。

#### 设置代理

如果没有代理，则可设置为`proxies = {"http":None, "https":None}`，如果需要使用代理，则设置为`        proxies = { "http": 'http://127.0.0.1:4780', "https": 'http://127.0.0.1:4780'}`，注意https中的地址为`http://127.0.0.1:4780`，而非`https://127.0.0.1:4780`

可以使用FacetheWorld这个VPN代理，当其中一个ip被封后，手动再换一个。



### 其他

#### 关于scrapy

scrapy用于管理多个爬虫，目前的实践中都是很小的爬虫，暂时用不上scrapy，听说scarpy的设计很巧妙，可以研读一下源码。



#### 相关文档

[Scrapy 2.5 documentation](https://docs.scrapy.org/en/latest/index.html)

[Requests: HTTP for Humans™](https://docs.python-requests.org/zh_CN/latest/)

[Beautiful Soup 4.4.0 文档](https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/#get-text)

