import re
import sqlite3


class SocietegeneraleluPipeline:
    conn = sqlite3.connect('societegeneralelu.db')
    cursor = conn.cursor()

    def open_spider(self, spider):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS `societegeneralelu` (
                                                                        title varchar(100),
                                                                        description text,
                                                                        date text
                                                                        )''')
        self.conn.commit()

    def process_item(self, item, spider):
        try:
            title = item['title']
            title = re.sub('"', "'", title).strip()
        except:
            title = ''
        try:
            description = item['description']
            description = re.sub('"', "'", description).strip()
        except:
            description = ''
        try:
            date = item['date'].strip()
        except:
            date = ''

        self.cursor.execute(f'''select * from societegeneralelu where title = "{title}" and date = "{date}"''')
        is_exist = self.cursor.fetchall()

        if len(is_exist) == 0:
            self.cursor.execute(
                f'''insert into `societegeneralelu` (`title`, `description`, `date`) values ("{title}", "{description}", "{date}")''')
            self.conn.commit()

        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()
