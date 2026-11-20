import base64
import requests
import re
import zlib

class KugouApi:
    SEARCH_URL = 'http://krcs.kugou.com/search'
    DOWNLOAD_URL = 'https://lyrics.kugou.com/download'

    def __init__(self, title, artist, duration=None): 
        self.title = title
        self.artist = artist
        self.duration = duration
        self.titles=[]

    def get_kugou_lrc(self):
        """
        获取酷狗歌词，如果未命中尝试去除括号后重试。
        """
        for attempt in range(3):
            keyword = self._build_keyword()
            duration = self.duration
            res = self._search_lrc(keyword,duration)
            if not res:
                return None

            candidates = res.get("candidates", [])
            for c in candidates:
                #result = self._select_best_candidate(candidates)
                #if result is not None:
                    id, accesskey = c["id"],c["accesskey"]
                    lyrics=self._download_best_lrc(id,accesskey)
                    lyrics,title,pos=self._remove_metadata(lyrics)
                    print("========================================================")
                    print()
                    print(f"{pos}) {title}")
                    print()
                    print(lyrics)
                    print()
            
            if attempt == 0:
                print("未命中歌词，尝试清理括号内容...")
                self._clean_metadata()
            elif attempt == 1:
                print("去除括弧后依旧未命中,尝试互换key...")
                temp = self.artist 
                self.artist = self.title
                self.title= temp
            else:
                print(f'最终未命中歌词!入参:{keyword},{duration}')

        return None

    def _build_keyword(self):
        return f"{self.artist} - {self.title}"

    def _search_lrc(self, keyword, duration):
        params = {
            'ver': '1',
            'man': 'yes',
            'client': 'mobi',
            'keyword': keyword,  # 👈 关键点！
            'duration': duration or '',
            'hash': '',
            'album_audio_id': ''
        }
        try:
            response = requests.get(self.SEARCH_URL, params=params)
            if response.status_code == 200:
                data = response.json()
                # with open("./search.json", "w", encoding="utf-8") as file:
                #     json.dump(data, file, indent=4, ensure_ascii=False)
                return data
        except Exception as e:
            print(f"请求出错: {e}")
        return None

    def _select_best_candidate(self, candidates):
        """
        从候选项中选出最优的 candidate，返回其 id 和 accesskey
        :param candidates: 搜索结果中的 candidates 列表
        :return: (id, accesskey) 或 None
        """
        try:
            best = min(
                candidates,
                key=lambda c: (
                    abs(c['duration'] // 1000 - self.duration // 1000) if self.duration else -c['score'],
                    -c['score']
                )
            )
            # print(f'歌曲id:{best["id"]},歌曲时长:{best["duration"]},歌曲评分:{best["score"]}')
            return best["id"], best["accesskey"]
        except (KeyError, ValueError, IndexError) as e:
            print(f"[候选选择错误] {e}")
            return None

    def _download_best_lrc(self, id,accesskey):
        try:
            params = {
                'ver': '1',
                'client': 'pc',
                'id': id,
                'accesskey': accesskey,
                'fmt': 'krc',
                'charset': 'utf8'
            }
            res = requests.get(self.DOWNLOAD_URL, params=params).json()
            lyrics = self._decode(base64.b64decode(res['content']))
            return self._fix_times(lyrics)
        except Exception as e:
            print(f"解析歌词出错: {e}")
            return None

    def _clean_metadata(self):
        self.title = self._remove_brackets(self.title)
        self.artist = self._remove_brackets(self.artist)

    @staticmethod
    def _remove_brackets(text):
        return re.sub(r'[\(\（\[\【\〔\{｛][^\)\）\]\】\〕\}｝]*[\)\）\]\】\〕\}｝]', '', text)

    def _decode(self,data):
        zd = bytes()
        krc_keys = [64, 71, 97, 119, 94, 50, 116, 71, 81, 54, 49, 45, 206, 210, 110, 105]
        for i in range(4, len(data)):
            zd += bytes([data[i] ^ krc_keys[(i - 4) % 16]])
        return zlib.decompress(zd).decode()

    def _fix_times(self,lyrics):
        lines=lyrics.split('\n')
        newlyrics=""
        for line in lines:
            time=re.search(r"\[\d+,\d+\]",line)
            if time != None:
                match=time.group()
                linespan=time.span()
                match=match.split(',')
                linetime=match[0][1:]
                wordtimes=re.findall(r"<\d+,\d+,\d+>",line)
                for i in range(len(wordtimes)):
                    wordtime=wordtimes[i].split(',')
                    wordtime=wordtime[0][1:]
                    wordtime=int(wordtime)
                    wordtime+=int(linetime)
                    wordtime=self._ms_to_time(wordtime)
                    line=re.sub(r"<\d+,\d+,\d+>","<"+wordtime+">",line,1)
                linetime=self._ms_to_time(linetime)
                line=re.sub(r"\[\d+,\d+\]","["+linetime+"]",line)
            newlyrics+=line+'\n'
        return newlyrics
        #what happens the lyrics are split into lines and find line time
        #line times=first num in []
        #word times=linetimes+first num in <>
        #convert from ms to mins:secs.ms and remove a digit for some reason
        #replace the ms nums with the new times
        #loop until all lines done

                
    def _ms_to_time(self,ms):
        ms=int(ms)
        mins=ms//60000
        ms-=mins*60000
        secs=ms//1000
        ms-=secs*1000
        ms=ms//10

        if mins == 0:
            mins="00"
        elif mins<10:
            mins="0"+str(mins)
        else:
            mins=str(mins)

        if secs== 0:
            secs="00"
        elif secs<10:
            secs="0"+str(secs)
        else:
            secs=str(secs)

        if ms ==0:
            ms="00"
        elif ms < 10:
            ms="0"+str(ms)
        else:
            ms=str(ms)

        return mins+":"+secs+"."+ms

    def _remove_metadata(self,olyrics):
        try:
            title=re.findall(r"\[ti:.*\]",olyrics)[0][4:-1]
        except IndexError:
            title="Title Unknown"
        self.titles.append(title)
        pos=len(self.titles)
        
        nlyrics=re.sub(r"\[[a-z]+:.*\]","",olyrics)
        return nlyrics, title, pos

    def print_titles(self):
        for i in range(len(self.titles)):
            print(f"{i+1}) {self.titles[i]}")
        
        
name=input("Enter name: ")
artist=input("Enter artist: ")
api = KugouApi(name, artist)
api.get_kugou_lrc()
api.print_titles()
