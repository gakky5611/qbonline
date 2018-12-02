# qbonline
pseudo_version of qbonline written by python

polls/modelsに

QuestionとSelectHistoryとPictureのモデルがある。
Pictureは完全に画像を扱うためのモデルで、Questionと1:Nの子関係
SelectHistoryはユーザーがある問題に関して、いつどういう答えを選んだかを表すモデルで、Questionと1:Nの関係
