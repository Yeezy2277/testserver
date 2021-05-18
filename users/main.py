
#from fpdf import FPDF, HTMLMixin


#class wow(FPDF, HTMLMixin):
#    pass

#html = '''
#<h1 style='color: red;'>Hello, dear 
#'''
#hz = 'gena'
#html += hz
#html += '</h1><p>qweodkwpeodkqw<br>peodkwieuwrhfiweourwerfewrfkweroifkweroifwerpoifhfeiwrufhwqepodkwqe[po<p>'

#pdf = wow()
#pdf.add_page()
#pdf.write_html(html)
#pdf.output('../wow.pdf')



import os 
import pathlib 

print(__file__)
print(pathlib.Path(__file__).resolve())
print(pathlib.Path(__file__).resolve().parent)
print(pathlib.Path(__file__).resolve().parent.parent)

print(os.path.dirname(pathlib.Path(__file__).resolve().parent.parent)) 

file_path = pathlib.Path(__file__).resolve().parent
path = os.path.join(str(file_path) + '/temporary', 'wow.txt')
os.remove(path)

print(file_path)

'''
file_path = pathlib.Path(__file__).resolve().parent + /temporary 


from fpdf import FPDF, HTMLMixin
class wow(FPDF, HTMLMixin):
    pass

text = '<h1>It is pdf document</h1>'

pdf = wow()
pdf.add_page()
pdf.write_html(text)
pdf.output(file_path + имя_пользователя + номер_договора + '.pdf')
сохранение в бд
удаление
'''

