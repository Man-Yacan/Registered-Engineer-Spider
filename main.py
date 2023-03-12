from selenium import webdriver
import time
import random
import re


# 创建一个爬虫类
class GetRegisteredEngineer(object):

    def __init__(self):
        '''
            对象初始化
        '''
        self.url = ''
        self.table_header = []
        self.Total_num_of_people = 123

    def run(self):
        '''
            类或对象入口函数
        '''
        select_index = self.print_info()
        self.get_web_gage()  # 发送请求
        self.select_group(select_index)  # 选择分组
        self.click_search()  # 点击查询
        while True:
            mark = self.get_element()  # 获取HTML元素
            self.get_next_page_btn()  # 获取下一页
            if mark == None:
                break
            else:
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

        # 如果表头数据为空则获取数据
        if len(self.table_header) == 0:
            first_tr = table.find_elements_by_xpath('.//tr[1]/td')  # 获取表头
            for td in first_tr:  # 将表头保存
                self.table_header.append(td.text)

        # 输出本页信息
        page_info_str = self.driver.find_element_by_id('labPageInfo').text
        print(page_info_str)

        info_tr = table.find_elements_by_xpath(
            './/tr[position()>1]')  # 获取所有剩下的信息行

        for tr in info_tr:
            temp_dict = {}
            tds = tr.find_elements_by_xpath('./td')
            for td in tds:
                temp_dict[self.table_header[tds.index(td)]] = td.text

            # 写入数据
            self.write_file(temp_dict)

        # 如果当前页序号等于全部页数，则说明数据爬取至最后一页了
        page_info_list = re.findall(r"\d+\.?\d*", page_info_str)
        if page_info_list[0] == page_info_list[1]:
            return None
        else:
            return 1

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
        # self.driver.execute_script('scrollTo(0,1000000)')  # 显示器较小时，需要滚动才能获取元素
        btn.click()

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
        print("本程序可以爬取中国*********网站\n中所有********.")
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
        print('='*40)
        # 获取并返回用户输入
        return int(input("请输入对应的功能序号："))


if __name__ == "__main__":
    my_spider = GetRegisteredEngineer()
    my_spider.run()