# -*- coding: utf-8 -*-

from pptx.util import Cm, Pt
from pptx.enum.text import PP_ALIGN, MSO_AUTO_SIZE, MSO_ANCHOR

class Poorscrum_Tasks:


    def __init__(self, slide, slide_height, slide_width, 
                 top = Cm(0.5), left = Cm(0.5), rows = 8, cols = 5):

        height = int(slide_height - 2*top)
        width = int(slide_width/2 - 2*left)

        #  There is only one placeholder currently
        idx = slide.shapes[0].placeholder_format.idx
        placeholder = slide.placeholders[idx]
        task_frame = placeholder.insert_table(rows,cols)
        table = task_frame.table
        
        table.first_row = False
        table.first_col = False
        table.last_row = True
        table.last_col = False

        """ Set the width of the columns """

        percents = [0.55, 0.1, 0.1, 0.1, 0.15]
        for col, percent in zip(table.columns, percents):
            col.width = int(percent*width)

        for row in table.rows:
            row.height = int(height/rows)

        default_text = ["<task{:d}>", "0", "0", "0", "<dev>"]        
        for rkey, row in enumerate(table.rows):
            
            for ckey, (cell, text) in enumerate(zip(row.cells, default_text)):
                t = cell.text_frame
                if ckey == 0:
                    t.word_wrap = True
                    t.auto_size = MSO_AUTO_SIZE.NONE
                    t.vertical_anchor = MSO_ANCHOR.TOP
                else:
                    t.word_wrap = False
                    t.auto_size = MSO_AUTO_SIZE.NONE
                    t.vertical_anchor = MSO_ANCHOR.MIDDLE

                p = t.paragraphs[0]
                if ckey == 0:
                    p.alignment = PP_ALIGN.LEFT
                else:
                    p.alignment = PP_ALIGN.CENTER

                r = p.add_run()
                r.text = default_text[ckey].format(rkey+1)
                r.font.size = Pt(10)
                r.font.name = 'Consolas'

        self.table = table

        
    def put_as_row(self, row, task):

        for cell, text in zip(self.table.rows[row].cells, task):
            t = cell.text_frame
            p = t.paragraphs[0]
            r = p.runs[0]
            r.text = text

            
    def put_as_list(self, tasks):

        for row, task in zip(self.table.rows, tasks):
            self.put_as_row(row, task)
            

    def get_from_row(self, row):
        return None

    
    def get_from_list(self):
        return None
    
