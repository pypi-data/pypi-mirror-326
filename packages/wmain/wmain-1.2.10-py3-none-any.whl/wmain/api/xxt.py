from wmain.requests import WSession, WUrl
from wmain.base import create_path
import re


class WAPI_XXT_Session:
    URL_API_COURSE_LIST_DATA = (
        "https://mooc2-ans.chaoxing.com/mooc2-ans/visit/courselistdata"
    )

    URL_MAIN = "https://chaoxing.com"
    WURL_FILE_LIST = WUrl(
        "https://mooc2-ans.chaoxing.com/mooc2-ans/coursedata/stu-datalist"
    )
    WURL_API_FILE_DOWNLOAD = WUrl(
        "https://mooc2-ans.chaoxing.com/mooc2-ans/coursedata/batchDownload"
    )
    XPATH_TEACHER_NAME = '//*[@class="course-info"]/p[2]/@title'
    XPATH_CLASS_NAME = (
        '//*[@class="course-info"]//*[@class="course-name overHidden2"]/@title'
    )
    XPATH_CLAZZ_ID = '//*[@class="clazzId"]/@value'
    XPATH_COURSE_ID = '//*[@class="courseId"]/@value'
    XPATH_FILE_TITLE = '//*[@class="dataBody_td"]/@dataname'
    XPATH_FILE_DATA_ID = '//*[@class="dataBody_td"]/@id'
    XPATH_FILE_T = '//*[@class="dataBody_td"]/@t'
    XPATH_FILE_TYPE = '//*[@class="dataBody_td"]/@type'
    RE_FILE_PAGE_NUM = re.compile('id="totalPages" value="(.*?)"')
    FILE_TYPE_FLODER = "afolder"

    def __init__(self, session: WSession):
        self.session = session
        self.downloading_filename = ""

    def login_by_cookie_str(self, cookie_str: str):
        self.session.load_cookies_str(cookie_str)
        self.flush()

    def login_by_cookie_editor(self, file: str):
        self.session.load_cookie_editor(file)
        self.flush()

    def flush(self):
        self._flush_class_teacher_classId_courseId_list()

    def _flush_class_teacher_classId_courseId_list(self) -> dict:
        data = {
            "courseType": "1",
            "courseFolderId": "0",
            "query": "",
            "pageHeader": "-1",
            "superstarClass": "0",
        }
        resp = self.session.post(self.URL_API_COURSE_LIST_DATA, data=data)
        teacher_list = resp.xpath(self.XPATH_TEACHER_NAME)
        clazz_list = resp.xpath(self.XPATH_CLASS_NAME)
        clazz_id_list = resp.xpath(self.XPATH_CLAZZ_ID)
        course_id_list = resp.xpath(self.XPATH_COURSE_ID)
        self.class_to_teacher_clazzId_courseId = {}
        for i in zip(clazz_list, teacher_list, clazz_id_list, course_id_list):
            self.class_to_teacher_clazzId_courseId[i[0]] = [i[1], i[2], i[3]]

    def _get_page_file_list(self, page: int) -> list:
        self.WURL_FILE_LIST["pages"] = str(page)
        resp = self.session.get(self.WURL_FILE_LIST)
        file_title_list = resp.xpath(self.XPATH_FILE_TITLE)
        file_data_id_list = resp.xpath(self.XPATH_FILE_DATA_ID)
        file_type_list = resp.xpath(self.XPATH_FILE_TYPE)
        return list(zip(file_title_list, file_data_id_list, file_type_list))

    def _get_page_num(self) -> int:
        self.WURL_FILE_LIST["pages"] = 1
        return int(
            self.RE_FILE_PAGE_NUM.findall(self.session.get(self.WURL_FILE_LIST).text)[0]
        )

    def _get_file_list(self) -> list:
        file_list = []
        for i in range(self._get_page_num()):
            file_list += self._get_page_file_list(i + 1)
        return file_list

    def _set_file_courseId_clazzId(self, class_name: str):
        self.WURL_FILE_LIST.params = ""
        v = self.class_to_teacher_clazzId_courseId[class_name]
        self.WURL_FILE_LIST["courseid"] = v[2]
        self.WURL_FILE_LIST["clazzid"] = v[1]

    def download_course_file(self, class_name: str, save_path: str, types: list = None):
        self._set_file_courseId_clazzId(class_name)
        self._download_file(self._get_file_list(), save_path, types)

    def _download_file(self, file_list: list, save_path: str, types: list = None):
        save_path = save_path.rstrip("/") + "/"
        create_path(save_path)
        for file_title, file_data_id, file_type in file_list:
            if file_type == self.FILE_TYPE_FLODER:
                _download_path = save_path + file_title + "/"
                self.WURL_FILE_LIST["dataName"] = file_title
                self.WURL_FILE_LIST["dataId"] = file_data_id
                self._download_file(self._get_file_list(), _download_path, types)
            else:
                if types and file_type not in types:
                    continue
                self.WURL_FILE_LIST["dataName"] = file_title
                self.WURL_FILE_LIST["dataId"] = file_data_id
                self.WURL_API_FILE_DOWNLOAD["classId"] = self.WURL_FILE_LIST["clazzid"]
                self.WURL_API_FILE_DOWNLOAD["courseId"] = self.WURL_FILE_LIST[
                    "courseid"
                ]
                self.WURL_API_FILE_DOWNLOAD["dataId"] = self.WURL_FILE_LIST["dataId"]
                download_url = self.session.get(self.WURL_API_FILE_DOWNLOAD).json[0]
                self.session.ini.headers["Sec-Fetch-Dest"] = "iframe"
                self.session.ini.headers["Sec-Fetch-Site"] = "same-site"
                self.session.ini.headers["Referer"] = self.URL_MAIN
                self.downloading_filename = save_path + file_title
                self.session.get(download_url).save(save_path + file_title)
                self.downloading_filename = ""


if __name__ == "__main__":
    s = WSession()
    s.ini.set_proxy(7890)
    xxt = WAPI_XXT_Session(s)
    xxt.login_by_cookie_str(
        """
lv=2; fid=2161; _uid=352782162; UID=352782162; vc=F026D56B559D8288F5FE3018E034335E; xxtenc=0ef9486958bfab4b71ccf51a30ffd30c; createSiteSource=num4; wfwfid=2161; workRoleBenchId=0; siteType=2; wfwEnc=33AF497C46C342DD5E66F60AB6A1B04A; vc2=70DD501C529D1BEE4F86028B82A275E0; uf=da0883eb5260151e2a2b147c9517a6bfda69ed3472ad704ed7d4049005bfb884749960c36febacfc4aa167e09ccf1fb7913b662843f1f4ad6d92e371d7fdf64407a35e9a674f5ad3fd68be96b6183b1af4751d19f3fc537abb6325cff18536b0d044429dc21abf45; _d=1732625467507; vc3=eMsDGrcL7lBop2Eh8xtHl4m4sT83g%2FVq1bXZDHpWX1FYYwQpfCBjwlsEEeZ7sA%2FA3thb3Y1vXSP4ZxCyeHZNAzOtSPFYv7xHOlBkaUX7oOkxEvhf1d6LZOjLyJCnlEnQzSyIGo9y2PYDJxmDX1KoWBNGlhLipUx44uRUYNDg6Ps%3Db8ab97baae0711c38e370494a7b7d823; cx_p_token=8221a7f0a3546545f04038824992be92; p_auth_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiIzNTI3ODIxNjIiLCJsb2dpblRpbWUiOjE3MzI2MjU0Njc1MDksImV4cCI6MTczMzIzMDI2N30.Xog1MXgqEEuYvuHTXkjYzrIeEI9wi2c817t247HRSA0; DSSTASH_LOG=C_38-UN_687-US_352782162-T_1732625467509; k8s=1732625725.759.12406.884827; jrose=B20BA908F2C1D3D48F3B59156B9467B3.mooc-3888598220-554ml; route=440ceb57420433374ff0504da9778fc7; thirdRegist=0; source=""; spaceFid=2161; spaceRoleId=""; fanyamoocs=9546D13B9AF931ECE4F8DE7C41ACEAB4; _dd352782162=1732625820379"""
    )
    xxt.download_course_file("系统解剖学", "./系统解剖学")
