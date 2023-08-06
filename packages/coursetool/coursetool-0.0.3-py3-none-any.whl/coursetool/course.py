#!/usr/bin python
#-*- coding:utf-8 -*-

import requests
import json
import re
import time
from bs4 import BeautifulSoup
import sys

__author__ = 'AnonymousJ'

TERM_PREFIX = '20172018010000'  # 本学期所有课程的前缀
class CourseInfo:
	def __init__(self, fields):
		self.class_id = fields[0]  # 教学班号码：课程id-班号
		self.uid = TERM_PREFIX + ''.join(self.class_id.split('-'))  # 课程唯一ID
		self.type = fields[1]  # 类型：公共基础课.etc
		self.name = fields[2]  # 课程名
		self.campus = fields[3]  # 在哪个校区
		self.weeks = fields[4]  # 哪几周上课
		self.score = int(fields[5])  # 学分
		self.level = int(fields[6])  # 等级：5/6/7
		self.total_num = int(fields[7])  # 限选总数
		self.current_num = int(fields[8])  # 当前实选人数
		self.detail = fields[9]  # 细节：上课时间地点等

	def __str__(self):
		return ','.join(list(map(str, [self.uid, self.type, self.name, self.current_num, self.total_num, self.detail])))
	
	__repr__ = __str__

# 登录获取cookie
def login(uid,upwd):
	login_url = 'http://gs.swjtu.edu.cn/pro/userscenter/login'
	form = {
		'userid' : uid,
		'userpwd' : upwd
	}
	r = requests.post(login_url,data=form)
	response = json.loads(r.text)
	if response['status'] == 'ok':
		print(response['msg'])
		return r.cookies

# 查看课程选取人数
def query_course(cid,login_cookie):
	url = 'http://gs.swjtu.edu.cn/ucenter/student/sheet/list_item/gep_course_selector'
	course = {
		'w_l_coursecode':cid,
		'page_size':30
	}
	extra = {
		'Referer': 'http://gs.swjtu.edu.cn/ucenter/student/home/index',
		'Origin': 'http://gs.swjtu.edu.cn',
		'User-Agent': 'Chrome60.0.3112.101'
	}
	r = requests.post(url,data=course,cookies=login_cookie, headers=extra)
	return r.text

# 解析返回的结果，只保留犀浦校区
def parse_result(doc):
	pat = re.compile(r'[\n\r\t\s]*([^\n\r\t\s]*)')
	soup = BeautifulSoup(doc,'lxml')
	# 表头
	headers = []
	for i in soup.find_all('th'):
		s = pat.match(i.text).group()
		if s != '':
			headers.append(s)
	# 表头固定不变，先不处理。
	# 数据
	infoLst = []
	for i in soup.find_all('tr'):
		if str(i).find('犀浦校区') != -1:
			tmp = []
			for j in i.find_all('td'):
				s = pat.match(j.text).group(1)
				if s != '':
					tmp.append(s)
			infoLst.append(CourseInfo(tmp))
	print('\n'.join(list(map(str, infoLst))))
	print('\n')
	return infoLst

# 选中某一门课，或者退选这门课
# course_uid 与course不同，他更长。
# selectOrdelete： Tru表示选课，False表示退课
def select_course(course_uid, login_cookie, selectOrdelete=True):
	action_str = 'gep_course_selector/selectcourse' if selectOrdelete else 'gep_course_select/delete'
	action_id = '001' if selectOrdelete else '0000'
	url = 'http://gs.swjtu.edu.cn/ucenter/student/sheet/exec_cmd/%s' % action_str
	form = {
		'cmd_d_key':course_uid,
		'role_actionid':action_id
	}
	extra = {
		'Referer': 'http://gs.swjtu.edu.cn/ucenter/student/home/index',
		'Origin': 'http://gs.swjtu.edu.cn',
		'User-Agent': 'Chrome60.0.3112.101'
	}
	r = requests.post(url,data=form,cookies=login_cookie, headers=extra)
	print(r.text)

def auto_delete():
	if len(sys.argv) != 4:
		print('退课，必须接3个参数\n\t用户名 密码 课程-班号\n 例如：course_delete 2020200333 123456 54013004-01\n\t以上代表这个用户退选54013004这门课的01教学班的课程')
		exit(0)
	cookies, uid = login(sys.argv[1],sys.argv[2]), TERM_PREFIX+''.join(sys.argv[3].split('-'))
	select_course(uid, cookies, False)

def auto_select():
	# 提示信息
	if len(sys.argv) != 6:
		print('抢课如抢票，错过第一波还有退课补全的机会，当有人退课时本py帮你自动填补空位\n')
		print('参数说明：必须接5个参数\n\t用户名 密码 课程ID 刷新间隔秒数 刷新上限次数(0或任意负数代表无限次)\n\t课程ID就是个人方案里课程名称前面那几个数字\n例如：course_select 2020200322 123456 54013004 30 1000\n\t代表每30秒刷新一次(最多1000次)高级数理统计课的人数并自动选择首先出现空位的教学班')
		print('\nPS：仅用于学习交流目的，不要其他用途，作者概不负责')
		exit(0)
	# 设定参数
	cookies, course_id, period, max_count = login(sys.argv[1],sys.argv[2]), sys.argv[3], int(sys.argv[4]), int(sys.argv[5])

	# 定时刷新人数并自动选则第一个教学班
	print('开始定时刷新并自动选课, 随时按ctrl+c停止')
	runningFlag, count = True, 0
	while runningFlag:
		infoLst = parse_result(query_course(course_id,cookies))
		for course in infoLst:
			if course.current_num < course.total_num:
				print('课程 %s 出现空位，帮你抢选啦' % str(course))
				select_course(course.uid, cookies)
				runningFlag = False
				print('目标达成，溜了')
				break
		time.sleep(period)

		if max_count != 0:
			count += 1
			if count == max_count:
				runningFlag=False
				print('到达最大刷新次数，停止')

def help():
	print('选课使用：auto_select命令')
	print('退课使用：auto_delete命令')