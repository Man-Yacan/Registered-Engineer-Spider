from selenium import webdriver
import time
import random


# 创建一个爬虫类
class GetRegisteredEngineer(object):

    def __init__(self):
        '''
            对象初始化
        '''
        self.url = 'http://219.142.101.79/regist/wfRegister.aspx?type=2'
        self.table_header = []

    def run(self):
        '''
            类或对象入口函数
        '''
        select_index = self.print_info()
        self.get_web_gage()  # 发送请求
        self.select_group(select_index)  # 选择分组
        self.click_search()  # 点击查询
        while True:
            self.get_element()  # 获取HTML元素
            btn_mark = self.get_next_page_btn()  # 获取下一页
            if btn_mark == None:
                break
            else:
                btn_mark.click()  # 获取下一页
                # 在一个页面随机停留5~20秒
                time.sleep(random.randint(5, 20))

        # 关闭浏览器
        self.driver.quit()

    def get_web_gage(self):
        '''
            发送请求
        '''
        self.driver = webdriver.Chrome()
        self.driver.get(self.url)
        # frame = self.driver.find_element_by_id('iframMain') # 根据id定位 frame元素
        # self.driver.switch_to.frame(frame) # 转向到该frame中

    def select_group(self, select_index):
        '''
            选择分组
        '''
        s1 = webdriver.support.ui.Select(
            self.driver.find_element_by_id('ddRType'))  # 实例化Select
        s1.select_by_index(select_index)  # 选择分组

    def get_element(self):
        '''
            获取HTML元素
        '''
        table = self.driver.find_element_by_id('dgEnterpriseList')  # 得到table
        first_tr = table.find_elements_by_xpath('.//tr[1]/td')  # 获取表头
        for td in first_tr:  # 将表头保存
            self.table_header.append(td.text)
        info_tr = table.find_elements_by_xpath(
            './/tr[position()>1]')  # 获取所有剩下的信息行
        for tr in info_tr:
            temp_dict = {}
            tds = tr.find_elements_by_xpath('./td')
            for td in tds:
                temp_dict[self.table_header[tds.index(td)]] = td.text
            # 写入数据
            self.write_file(temp_dict)

    def click_search(self):
        '''
            点击查询
        '''
        search_btn = self.driver.find_element_by_id('Button1')
        search_btn.click()

    @staticmethod
    def write_file(txt):
        '''
            写入文件
        '''
        with open('GetRegistered.data', 'a+', encoding='utf-8') as f:
            f.write(str(txt))
            f.write(',\n')

    def get_next_page_btn(self):
        '''
            获取下一页按钮
        '''
        btn = self.driver.find_element_by_id('LinkButton3')
        # self.driver.execute_script('scrollTo(0,1000000)')  # 页面较长，需要滚动才能获取元素

        try:
            end_mark = self.driver.find_element_by_xpath(
                '//*[@id="dgEnterpriseList"]/tbody/tr[11]/td[1]')
        except:
            pass
        else:
            if (end_mark.text == '14510'):  # 截止到2020年8月24日全国注册给排水工程师共有14510名
                return None
            else:
                return btn

    @staticmethod
    def print_info():
        '''
            打印提示信息
        '''
        print('='*40)
        print(' 欢迎使用本程序 '.center(33, '+'))
        print('='*40)
        print(" 程序功能：".center(35, '+'))
        print('='*40)
        print("本程序可以爬取中国建设部网上办事大厅网站\n中所有勘察设计工程师信息.")
        print('='*40)
        print(" 警告信息：".center(35, '+'))
        print('='*40)
        print("本程序仅仅用作个人编程学习，严禁在非涉密\n网络及上网计算机上发布、处理和传输涉密信\n息！")
        print('='*40)
        print(" 运行环境：".center(35, '+'))
        print('='*40)
        print("本程序基于Python 3.7.2 64-bit windows平台")
        print('='*40)
        print(" 选择列表：".center(35, '+'))
        print('='*40)
        print("1：一级注册结构工程师")
        print("2：注册土木工程师（岩土）")
        print("3：注册公用设备工程师（暖通空调）")
        print("4：注册公用设备工程师（给水排水）")
        print("5：注册公用设备工程师（动力）")
        print("6：注册电气工程师（发输变电）")
        print("7：注册电气工程师（供配电）")
        print("8：注册化工工程师")
        print('='*40)
        # 获取并返回用户输入
        return int(input("请输入对应的功能序号："))


if __name__ == "__main__":
    my_spider = GetRegisteredEngineer()
    my_spider.run()
