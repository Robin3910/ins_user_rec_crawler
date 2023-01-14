import openpyxl
from openpyxl.drawing.image import Image

data = [['username', 'fans', 'desc', 'country'], ['jemsplaytime', 10493,
                                                  'JeMplaytime-Toys and moreGames/toysWe review toys and more. Helping find the perfect toys, games and fun places is our goal.Acct run by Mum. DM for collab/PR♥️👉 click link for more linktr.ee/jemsplaytime',
                                                  'United Kingdom'], ['busyhands_busybrain', 840,
                                                                      'Bruna GalloEducation@busyhands_busybrain Uma educadora pelo mundo.🇧🇷🇮🇹🇦🇺🇺🇸🇳🇿🎓Pedagoga- USP/Brasil📚Mestra em Educação Infantil- USP/Brasil👫Mãe de 2 💕 open.spotify.com/show/2wrG7IQogjK0zpsZoV7v73?si=3tyeux0QRJKBOPZ3y4-KaA',
                                                                      '']]
workbook = openpyxl.Workbook()
sheet = workbook.active
for i in range(1, len(data)):
    row = data[i]
    sheet.append(row)
    img = Image(f'../imgs/{row[0]}.jpg')
    img.width = 50
    img.height = 50
    sheet.add_image(img, f'E{i}')

    # post imgs
    for j in range(0, 2):
        postImg = Image(f'../imgs/{row[0]}_{j}.jpg')
        postImg.width = 50
        postImg.height = 50

        boxPos = ''
        if i == 0:
            boxPos = f'F{i}'
        if i == 1:
            boxPos = f'G{i}'
        if i == 2:
            boxPos = f'H{i}'

        sheet.add_image(postImg, boxPos)

workbook.save('userinfo.xlsx')
print("get userinfo task finish, save into excel")
