# -*- coding: utf-8 -*-
import os
import time
from keywordgroup import KeywordGroup
from robot.api import logger
from selenium.webdriver.common.action_chains import ActionChains
try:
	import SendKeys
except ImportError:
	# try to import other lib for target OS platform
	pass
try:
	import win32gui
except ImportError:
	# try to import other lib for target OS platform
	pass


class _WebKeywords(KeywordGroup):

	def __init__(self):
		self._web_gen_gif = False


	def web_Set_gif_flag(self, web_gif_flag="FALSE"):
		""" Set Web GIF Generation Flag. (Default: "FALSE" / "TRUE": generate one GIF file for each TestCase)
		设置用例生成GIF开关.(默认设置为"FALSE", 当设置为“TRUE/True”时， 每个用例都会生成一份同名的gif文件)
		This KW will invoke at Library importing, Also Can be invoked during case running.
		| Web Set Gif Flag | TRUE | #enable genrate gif for test case |
		| Web Set Gif Flag | FALSE | #disable genrate gif for test case  |
		"""
		if web_gif_flag.upper() == "TRUE":
			self._web_gen_gif = True
		else:
			self._web_gen_gif = False

	# Public Web Keywords
	def web_hover_and_click(self, elementToHover_locator, elementToClick_locator, elementToHover_selected_num=1, elementToClick_selected_num=1):
		"""Hover and click ，复合操作命令
		elementToHover_locator:       同Selenium2Library里的locator, 指定hover目标元素-hover的区域位置.
		elementToClick_locator:       同Selenium2Library里的locator, 指定hover后出现的目标元素-要点击的元素位置.
		elementToHover_selected_num:  指定hover目标元素序号.
		elementToClick_selected_num:  指定hover后出现的目标元素序号.
		[不输入（默认值）:  点击第一个元素];
		[=0 :               点击最后一个元素]; 
		[=x（>0）:          点击第x个元素].


		一般使用方法：
		| Web Hover And Click | xpath=//div[3]/ul/li[1] | xpath=//div[3]/ul/li[1]/span[2]/a[3] |
		| Web Hover And Click | ${elementToHover_locator} | ${elementToClick_locator} |
		带seleted_num使用方法：
		注意 locators的xpath表达方式以及seleted_num的设定，需要保持hover元素和点击元素的一致性
		| Web Hover And Click | xpath=//div/div[3]/ul/li | xpath=//span[2]/a[3] | 2 | 2 |
		| Web Hover And Click | ${elementToHover_locators} | ${elementToHover_locators} | 0 | 0 |
		(在运行该KW会将浏览器窗口移到你看不到的地方，以后也别想看到，屏幕截图是好的，哈哈~~)
		"""
		#self._current_browser().set_window_size(100, 100)#设置窗口大小
		self._current_browser().set_window_position(-10000, -10000)#设置窗口位置将窗口移出桌面。。。
		self._info("Hover '%s' and click '%s'" % (elementToHover_locator, elementToClick_locator))
		elementToHover = self._get_selected_element(elementToHover_locator, elementToHover_selected_num)
		elementToClick = self._get_selected_element(elementToClick_locator, elementToClick_selected_num)
		if elementToHover is None:
			raise AssertionError("ERROR: Element %s not found." % (elementToHover_locator))
		if elementToClick is None:
			raise AssertionError("ERROR: Element %s not found." % (elementToClick_locator))
		actions = ActionChains(self._current_browser())
		actions.move_to_element(elementToHover)
		#actions.move_to_element(elementToClick)
		actions.click(elementToClick)
		actions.perform()
		self._current_browser().set_window_position(0, 0)#移回来了。。

	def web_upload_file(self, filepath):
		"""上传文件(用于flash上传控件)

		filepath 文件路径，支持绝对路径和相对路径，注意写法，例如：${CURDIR}${/}Res${/}Plus_Web${/}pic0.jpg
        ${CURDIR}指数据所在文件的当前路径
		RF中filepath的写法被认为是unicode
		另外，这里的输入依赖系统的输入法，建议提前切换至英文，用美式键盘最好
		| Web Upload File | ${filepath} |	
		| Web Upload File | ${CURDIR}${/}Res${/}Plus_Web${/}pic0.jpg | 	
		"""
		filepath=os.path.abspath(filepath)
		change = str(filepath)
		time.sleep(1)
		self._handle = win32gui.FindWindow(None, u"打开")#获取“打开”窗口的句柄
		win32gui.SetForegroundWindow(self._handle)#聚焦当前窗口
		SendKeys.SendKeys(change)
		time.sleep(1)
		SendKeys.SendKeys("{ENTER}")

	def web_open_browser(self, url, browser='chrome', alias=None, remote_server_url=False, desired_capabilities=None, **kwargs):
		"""打开浏览器
		url:     URL路径（必填）
		browser: 浏览器类型，默认为Chrome浏览器 （可选）
		        | chrome           | Google Chrome |
        		| googlechrome     | Google Chrome |
        		| gc               | Google Chrome |
        		| firefox          | FireFox   |
       			| ff               | FireFox   |
        		| internetexplorer | Internet Explorer |
        		| ie               | Internet Explorer |
        		| opera            | Opera         |
        		| safari           | Safari        |
		alias:   别名，默认为空/None （可选）
		remote_server_url:  Selenium (Grid) Server Url, 默认为不启用/False （可选）
		desired_capabilities:  （可选） 必须与remote_url一起使用
				可参考https://github.com/SeleniumHQ/selenium/wiki/Grid2 
				capability.setBrowserName(“firefox” ); 
				capability.setPlatform(“LINUX”);  
				browserName:firefox,platform:LINUX

        本地运行：
		| Web Open Browser | ${url} |
		| Web Open Browser | http://www.163.com |
		| Web Open Browser | http://www.163.com | firefox |
		远程Server运行：
		| Web Open Browser | http://www.163.com | remote_url=http://localhost:4444/wd/hub | desired_capabilities=${capabilities} |
		| Web Open Browser | http://www.163.com | remote_url=http://localhost:4444/wd/hub | desired_capabilities=browserName:firefox,platform:LINUX |
		"""		
		self.open_browser(url, browser=browser, alias=alias, remote_url=remote_server_url, desired_capabilities=desired_capabilities, **kwargs)

	def web_close_browser(self):
		"""关闭当前浏览器

		| Web Close Browser |
		"""
		self.close_browser()

	def web_close_all_browsers(self):
		"""关闭所有浏览器,用在多个浏览器打开后

		| Web Open Browser | http://www.163.com |
		| Web Open Browser | http://www.google.com |
		| Web Close All Browsers |
		"""
		self.close_all_browsers()

	def web_click_element(self, locator, selected_num=1):
		"""点击元素操作（locator搜索结果为多个元素时，默认点击其中第一个，可以设定target_num，点击指定第n元素）
        locator: 同Selenium2Library里的locator;
        selected_num: 指定元素序号.
        [不输入（默认值）:   点击第一个元素]
        [=0 :              点击最后一个元素]
        [=x（>0）:          点击第x个元素]

		locator 同Selenium2Library里的locator
		| Web Click Element | ${locator} | ${selected_num} |
		| Web Click Element | id=username | 2 |
	    locator 示例:
    	| identifier | Click Element `|` identifier=my_element | Matches by @id or @name attribute               |
    	| id         | Click Element `|` id=my_element         | Matches by @id attribute                        |
    	| name       | Click Element `|` name=my_element       | Matches by @name attribute                      |
    	| xpath      | Click Element `|` xpath=//div[@id='my_element'] | Matches with arbitrary XPath expression |
		"""		
		selected_element = self._get_selected_element(locator, selected_num)
		selected_element.click()

	def web_click_text_button(self, text, selected_num=1):
		"""点击可以通过按钮内文字定位的文本/按钮（Button/Link）元素（相同文字的按钮为多个元素时，默认点击其中第一个，可以设定target_num，点击指定第n元素）
        text: 为按钮内的文字, 比如： 欢迎页－登录平台  主菜单页－群发消息/分组管理
        target_num: 指定元素（按钮）序号
        [不输入（默认值）:  点击第一个元素]
        [=0 :             点击最后一个元素]
        [=x（>0）:         点击第x个元素]

		text 为按钮内的文字
		如下的控件可以使用：<a href="/mass">群发消息</a> 或 <input id="submit-button" type="button" class="submit u-btn" value="快速登录平台">
		<button>中&nbsp;文</button>
		| Web Click Text Button | ${text} | ${selected_num} |
		| Web Click Text Button | 群发消息 | 2 |
		| Web Click Text Button | 中&nbsp;文 |
		"""
		# change '&nbsp;' to unicode string '\u00a0'
		h_space = u"&nbsp;"
		u_space = u"\u00a0"
		if h_space in text:
			text = text.replace(h_space, u_space)

		#选择Exactly Match 方法 xpath=//*[text()='%s'] % text
		#common_locator = u"xpath=//*[contains(text(), '%s')]"  % text
		common_locator = u"xpath=//*[text()='%s']" % text

		if self.web_get_elements_num(common_locator) > 0:
			# 元素查询尝试1 text 方式： 所有标签（包括<a>标签 or 类<a>标签）的text值
			self.web_click_element(common_locator, selected_num)
		else:
			common_locator = "xpath=//*[@value='%s']" % text
			if self.web_get_elements_num(common_locator, timeout=1) > 0:
				# 元素查询尝试2 value属性 方式：所有标签 属性中的 value值
				self.web_click_element(common_locator, selected_num)
			else:
				# 元素查询尝试3 link 方式（自动过滤一些空格）
				common_locator = 'link=' + text
				self.web_click_element(common_locator, selected_num)



	def web_input_text(self, locator, text, withenter='no'):
		"""向文本框中输入文本

		locator 同Selenium2Library里的locator
		text 用户名
		withenter 是否在最后按下Enter，默认是no
		| Web Input Text | ${locator} | ${text} |
		| Web Input Text | ${locator} | ${text} | ${withenter} |
		| Web Input Text | id=username | myaccount |
		| Web Input Text | id=username | myaccount | yes |
		"""
		self.wait_until_page_contains_element(locator)
		self.input_text(locator, text)
		if withenter.lower() == 'yes':
			self.press_key(locator, '\\13')

	def web_input_password(self, locator, password):
		"""向文本框中输入密码

		locator 同Selenium2Library里的locator
		password 密码
		| Web Input Password | ${locator} | ${password} |
		| Web Input Password | id=password | mypassword |
		"""
		self.wait_until_page_contains_element(locator)
		self.input_password(locator, password)

	def web_choose_file(self, locator, filepath):
		"""处理页面元素中input类型是file的元素，用来上传文件

		locator 同Selenium2Library里的locator
		filepath 文件路径，支持绝对路径和相对路径，注意写法
		| Web Choose File | ${locator} | ${filepath} |
		| Web Choose File | id=upload | ${CURDIR}${/}Res${/}Plus_Web${/}pic0.jpg |
		"""
		filepath=os.path.abspath(filepath)
		self.wait_until_page_contains_element(locator)
		self.choose_file(locator, filepath)

	def web_select_frame(self, locator, selected_num=1):
		"""选locator定位的frame为当前的frame
		
		locator 同Selenium2Library里的locator
		selected_num 可以不填，默认是1，选取匹配的第一个元素
		| Web Select Frame | ${locator} | ${selected_num} |
		| Web Select Frame | name=iframe | 2 |
		"""
		selected_frame = self._get_selected_element(locator, selected_num)
		self._current_browser().switch_to_frame(selected_frame)

	def web_unselect_frame(self):
		"""设置顶层frame为当前frame

		| Web Unselect Frame | |
		"""
		self.unselect_frame()

	def web_click_chosen_element(self, locator, chosen_num=1):
		"""选择符合条件:locator定义的第chosen_num个元素，并点击它，与Web Click Element功能一致，推荐用Web Click Element

		locator 元素定位
		chosen_num 符合的第chosen_num个元素，默认是1，选取匹配的第一个元素
		| Web Click Chosen Element | ${locator} | ${chosen_num} |
		| Web Click Chosen Element | id=myid | 2 |
		"""
		selected_element = self._get_selected_element(locator, chosen_num)
		selected_element.click()

	def web_confirm_alert_ok(self):
		"""对弹出的确认对话框选择OK

		| Web Confirm Alert Ok | |
		"""
		logger.info("点击Alert框确定按钮")
		self.confirm_action()

	def web_confirm_alert_cancel(self):
		"""对弹出的确认对话框选择取消

		| Web Confirm Alert Cancel| |
		"""
		logger.info("点击Alert框取消按钮")
		self.choose_cancel_on_next_confirmation()#设置_cancel_on_next_confirmation为True
		self.confirm_action()

	def web_page_screenshot(self, filename=None):
		"""截屏

		filename 自定义文件名
		| Web Page Screenshot | ${filename} |
		| Web Page Screenshot |  |
		| Web Page Screenshot | pic1 |
		"""
		self.capture_page_screenshot(filename)

	def web_select_from_list(self, locator, *value):
		"""选择下拉框

		locator 元素位置
		value 下拉框中的对应值
		| Web Select From List | ${locator} | ${value} |
		"""
		self.wait_until_page_contains_element(locator)
		self.select_from_list(locator, *value)
		

	def web_get_text(self, locator, selected_num=1):
		"""获取locator位置的text对应值（locator搜索结果为多个元素时，默认选择其中第一个，可以设定selected_num，指定第n元素）
        selected_num: 指定元素序号.
        [不输入（默认值）:  点击第一个元素]
        [=0 :             点击最后一个元素]
        [=x（>0）:         点击第x个元素]

		locator 同Selenium2Library里的locator
		| Web Get Text | ${locator} |
		| Web Get Text | id=myid |
		| ${button_num} | Web Get Text | id=myid |
		| ${button_num} | Web Get Text | xpath=//*[@class='col col-at j-number'] | 2 |
		"""
		element = self._get_selected_element(locator, selected_num)
		return element.text

	def web_get_title(self):
		"""获取当前页面的标题

		| Web Get Title | |
		"""
		return self.get_title()

	def web_get_value(self, locator, selected_num=1):
		"""获取locator元素的value值，通常可以用此获取Input控件的内容（locator搜索结果为多个元素时，默认选择其中第一个，可以设定selected_num，指定第n元素）
        selected_num: 指定元素序号.
        [不输入（默认值）:  点击第一个元素]
        [=0 :             点击最后一个元素]
        [=x（>0）:         点击第x个元素]

		locator 同Selenium2Library里的locator
		| Web Get Value | ${locator} |
		| Web Get Value | name=email | # 获取输入框已输入的内容 |
		| ${Input_Value} | Web Get Value | name=mobile |
		| ${Input_Value} | Web Get Value | name=mobile | 1 |
		"""
		element = self._get_selected_element(locator, selected_num)
		return element.get_attribute('value')

	def web_get_element_attribute(self, locator, attribute, selected_num=1):
		"""获取locator元素的属性值，可以是各种属性(value/name/preholder/class)（locator搜索结果为多个元素时，默认选择其中第一个，可以设定selected_num，指定第n元素）
        selected_num: 指定元素序号.
        [不输入（默认值）:  点击第一个元素]
        [=0 :             点击最后一个元素]
        [=x（>0）:         点击第x个元素]

		locator 同Selenium2Library里的locator
		| Web Get Element Attribute | ${locator} | value | # 获取输入框已输入的内容 |
		| Web Get Element Attribute | name=username | placeholder | # 获取输入框默认提示内容 |
		| ${Input_Value} | Web Get Element Attribute | id=account | value | 0 |
		| ${Input_placeholder} | Web Get Element Attribute | id=password | placeholder | 1 |
		"""
		element = self._get_selected_element(locator, selected_num)
		return element.get_attribute(attribute)

	def web_maximize_browser_window(self):
		"""最大化浏览器窗口

		| Web Maximize Browser Window |
		"""
		self.maximize_browser_window()

	def web_go_to(self, url):
		"""跳转到提供的url

		| Web Go To | ${url} |
		| Web Go To | http://www.163.com |
		"""	
		self.go_to(url)

	# Verification KWs
	def web_page_should_contain(self, text):
		"""验证当前页面是否包含text(自含等待timeout(库设置))

		text 页面包含的文本
		| Web Page Should Contain | ${text} |
		| Web Page Should Contain | Hello! |
		"""
		self.web_wait_until_text_exist(text)
		self.page_should_contain(text)

	def web_page_should_not_contain(self, text):
		"""验证当前页面是否包含text(自含等待timeout(库设置))

		text 页面不包含的文本
		| Web Page Should Not Contain | ${text} |
		| Web Page Should Not Contain | Hello! |
		"""
		self.web_wait_until_text_vanish(text)
		self.page_should_not_contain(text)
	
	def web_page_should_contain_element(self, locator):
		"""验证当前页面是否包含locator定位的元素(自含等待timeout(库设置))

		locator 元素定位
		| Web Page Should Contain Element | ${locator} |
		| Web Page Should Contain Element | id=myid |
		""" 
		self.web_wait_until_element_exist(locator)
		self.page_should_contain_element(locator)

	def web_page_should_not_contain_element(self, locator):
		"""验证当前页面是否包含locator定位的元素(自含等待timeout(库设置))

		locator 元素定位
		| Web Page Should Not Contain Element | ${locator} |
		| Web Page Should Not Contain Element | id=myid |
		""" 
		self.web_wait_until_element_vanish(locator)
		self.page_should_not_contain_element(locator)

	# Wait KWs
	def web_wait_until_text_exist(self, text, timeout=None):
		"""timeout时间内，等待至当前页面包含text

		text 页面包含的文本
		timeout 设置等待时间(s)，默认值为库设定值
		| Web Wait Until Text Exist | ${text} |
		| Web Wait Until Text Exist | Hello! |
		"""
		self.wait_until_page_contains(text, timeout)

	def web_wait_until_text_vanish(self, text, timeout=None):
		"""timeout时间内，等待至当前页面不包含text

		text 页面不包含的文本
		timeout 设置等待时间(s)，默认值为库设定值
		| Web Wait Until Text Vanish  | ${text} |
		| Web Wait Until Text Vanish | Hello! |
		"""
		self.wait_until_page_does_not_contain(text, timeout)
	
	def web_wait_until_element_exist(self, locator, timeout=None):
		"""timeout时间内，等待至当前页面包含locator指定的元素

		locator 元素定位
		timeout 设置等待时间(s)，默认值为库设定值
		| Web Wait Until Element Exist | ${locator} |
		| Web Wait Until Element Exist | id=myid |
		""" 
		self.wait_until_page_contains_element(locator, timeout)

	def web_wait_until_element_vanish(self, locator, timeout=None):
		"""timeout时间内，等待当前页面不包含locator指定的元素

		locator 元素定位
		timeout 设置等待时间(s)，默认值为库设定值
		| Web Wait Until Element Vanish | ${locator} |
		| Web Wait Until Element Vanish | id=myid |
		""" 
		self.wait_until_page_does_not_contain_element(locator, timeout)


	def web_execute_javascript(self, *code):
		"""执行javascript代码

		代码可能错误，需要修改
		| Web Execute Javascript | ${*code} |
		| Web Execute Javascript | window.document.getElementById('foo') |
		"""
		return self.execute_javascript(*code)	

	def web_get_alert_message(self):
		"""返回当前JavaScript alert的text

		| Web Get Alert Message | |
		"""
		return self.get_alert_message()

	def web_select_window(self, locator=None):
		"""选择窗口

		请结合Web Get Title使用
		| Web Select Window | ${locator} |
		| *Strategy* | *Example*                               | *Description*                        |
        | title      | Select Window `|` title=My Document     | Matches by window title              |
        | name       | Select Window `|` name=${name}          | Matches by window javascript name    |
        | url        | Select Window `|` url=http://google.com | Matches by window's current URL      | 
		"""
		self.select_window(locator)	

	# 后添加KW，可用性不强
	def web_get_elements_num(self, locator, timeout=None):
		"""返回符合locator定义的元素的个数 0-n
        locator: 同AppiumLibrary里的locator;

		| Web Get Elements Num | ${locator} |
		| Web Get Elements Num | id=myid |
		| ${element_num} | Web Get Elements Num | id=myid |
		"""		
		try:
			self.wait_until_page_contains_element(locator, timeout)
			elements_list = self.get_webelements(locator)
		except Exception:
			#raise AssertionError("ERROR: Element %s not found." % (locator))
			return 0		
		return len(elements_list)

	def web_get_element_isDisplayed(self, locator):
		"""返回locator定位的元素是否可见，返回True或者false

		| Web Get Element IsDisplayed | ${locator} |
		| Web Get Element IsDisplayed | xpath=//div[@class='edit-btn'] |
		"""
		element = self._element_find(locator, True, False)
		return element.is_displayed()

	def web_get_text_button_num(self, text):
		"""返回匹配‘text’的文本/按钮（Button/Link）元素的个数 0-n
		text: 为按钮、Link元素内的文字, 比如： 登录  退出  查找

		| Web Get Text Button Num | ${text} |
		| Web Get Text Button Num | 登录 |
		| ${button_num} | Web Get Text Button Num | 15500000001 |
		| ${button_num} | Web Get Text Button Num | 登 录 |
		| ${button_num} | Web Get Text Button Num | 确 \ 认 |
		"""
        # 元素查询尝试1 text 方式： 所有标签（包括<a>标签 or 类<a>标签）的text值
		common_locator = "xpath=//*[text()='%s']" % text
		button_num = self.web_get_elements_num(common_locator)
		# 元素查询尝试2 value属性 方式（<a>标签 or 类<a>标签中的 value值）
		common_locator = "xpath=//*[@value='%s']" % text
		return button_num + self.web_get_elements_num(common_locator, timeout=1) 

	def _get_selected_element(self, locator, selected_num=1):
		"""返回选中的元素

		locator 元素位置
		selected_num 元素序号，从1开始
		"""
		self.wait_until_page_contains_element(locator)
		index = int(selected_num) - 1
		elements_list = self.get_webelements(locator)
		if index < len(elements_list):
			return elements_list[index]
		else:			
			raise AssertionError("ERROR: Element selected_num %d is out of the length of elements_list" % int(selected_num))