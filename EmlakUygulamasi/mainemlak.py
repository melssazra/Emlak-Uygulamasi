# -*- coding: utf-8 -*-
"""
Created on Sun May 26 05:29:54 2024

@author: mat76
"""

import sys
from PyQt5 import QtCore, QtGui,QtWidgets
from PyQt5.QtWidgets import QMessageBox,QTableWidgetItem
from EmlakUygulamasiWidgets import  Ui_Mw_emlak1
from sifrearayuzuWidgets import Ui_mw_sifre  #sifrearayüzüwidgetsi.py dosyasından içeri aktar
from hakkindaWidgets import Ui_mw_hakkinda  #hakkindaWidgets.py dosyasını içeri aktar
import sqlite3,os #dosya veya dizin varlığını kontrol etmek için os modülünü import ediyoruz

class mw_hakkinda_class(QtWidgets.QMainWindow, Ui_mw_hakkinda):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.resim()
    
    #hakkında bölümünde olan görseli program çalıştığında sorunsuz görünmesini sağalar
    
    def resim(self):
        image="C:\/Users/mat76/OneDrive/Masaüstü/EmlakUygulamasi/ev.png" 
        
        #dizinin yolunun var olupolmadığını kontrol et
        if not os.path.exists(image): 
            print(f"Error:{image} dosya mevcut değil")
            return
        
        #görseli yükleyip piksel kontrolü yap
        pix=QtGui.QPixmap(image)
        if pix.isNull():
            print(f"Error: {image} dosyasında piksel hatası")

        self.label.setPixmap(pix)
        self.label.setScaledContents(True)  #resmin label'a sığacak şekilde ölçeklenmesi        

class mw_sifre_class(QtWidgets.QMainWindow, Ui_mw_sifre):
    def __init__(self):
        super().__init__()
        self.ui=Ui_mw_sifre()
        self.setupUi(self)
        self.pb_giris.clicked.connect(self.giris_ekrani)
        self.pb_cikis.clicked.connect(self.cikis_ekrani)
        
    def giris_ekrani(self):
        
        kullaniciadi=self.lne_kullaniciadi.text()
        sifre=self.lne_sifre.text()
        if kullaniciadi == "MAT" and sifre =="345508": #kullanıcının bilgileri
            QMessageBox.information(self,"BAŞARILI","HOŞGELDİN, MAT !")
            self.anaprogram() #anaprogram fonksiyonuna yönlendirilir 
     
        else:
            QMessageBox.warning(self,"UYARI","Yanlış bilgi girdiniz!")
           
    #Ana programla uyumlama fonksiyonu
    def anaprogram(self):
        self.ana_p=Mw_emlak1_class() #tanımlama
        self.ana_p.show()  #görüntüleme
        self.close()

    def cikis_ekrani(self):
        self.close()
    
    

class Mw_emlak1_class(QtWidgets.QMainWindow,Ui_Mw_emlak1):
    global conn
    global curs
    def __init__(self):
        super(Mw_emlak1_class,self).__init__()
        self.setupUi(self)
        self.baglanti_olustur()
        self.listele()
        self.pb_kayitekle.clicked.connect(self.kayit_ekle)
        self.pb_kayitekle.clicked.connect(self.listele)
        self.pb_kayitsil.clicked.connect(self.kayit_sil)
        self.pb_kayitsil.clicked.connect(self.listele)
        self.pb_kayitara.clicked.connect(self.kayit_ara)
        self.pb_kayitguuncelle.clicked.connect(self.guncelle)
        self.pb_kayitguuncelle.clicked.connect(self.listele)
        self.pushButton.clicked.connect(self.listele)
        self.pb_cikis.clicked.connect(self.cikis)
        self.tbl_liste.itemSelectionChanged.connect(self.doldur)
        
        #Telefon numarası 
        telefon = QtCore.QRegExp(r"\d{3}\ \d{3}\ \d{4}") 
        telefonv=QtGui.QRegExpValidator(telefon,self.lne_evshbtelefon)
        self.lne_evshbtelefon.setValidator(telefonv)
        self.lne_evshbtelefon.setInputMask("000 000 0000") #telefon numarası düzeni 
        
        self.tbl_liste.setShowGrid(True) #tablo çizgileri

    def veri_giris_kontrol(self,ad_soyad,tel_no):
        #ad-soyad kobtrol
        if not ad_soyad.replace(" ","").isalpha():
            QMessageBox().warning(self,"UYARI","Ad soyad yalnızca harf içermelidir")
            return False
         
        #telno kontrol
        if not self.telefon_format_kontrol(tel_no):
            QMessageBox.warning(self, "UYARI", "Telefon numarası doğru formatta değil")
            return False
        
        return True
    
    def telefon_format_kontrol(self, telefon_numarasi):
        
        # Telefon numarasının uzunluğunu kontrol et
        if len(telefon_numarasi) != 12:
            return False
    
        # Metni boşluklara göre ayır ve her bir parçanın tamamen rakam içerdiğinden emin ol
        telefon_parcalari = telefon_numarasi.split()
        for parca in telefon_parcalari:
            if not parca.isdigit():
                return False
    
        # Eğer tüm kontrollerden geçtiyse doğru formatta bir telefon numarası olduğunu belirt
        return True


    def kayit_ekle(self):
        #widget bilgilerinin formdan alınması
        _lneTelno=self.lne_evshbtelefon.text()
        _lneadSoyad=self.lne_evshbad.text()
        _lneemail=self.lne_evshbmail.text()
        _lne_kat=self.lne_kat.text()
        _lne_alan=self.lne_alan.text()
        _lne_odas=self.lne_odasayisi.text()
        _lne_binay=self.lne_binaninyasi.text()
        _lne_ilce=self.lne_ilanilce.text()
        _lne_adres=self.lne_adres.text()
        
        
        #girilen telno ve adsoyadı kontrol ettir
        if not self.veri_giris_kontrol(_lneadSoyad,_lneTelno):
            return
        
        
        #radio button seçim
        if self.rdb_kiralik.isChecked():
            Ev_Durumu="Kiralık"
        elif self.rdb_satilik.isChecked():
            Ev_Durumu="Satılık"
        else:
            Ev_Durumu="Belirtilmemiş"
            

        
        _cmb_ulasim=self.cmb_evshbulasim.currentText()
        _cmb_konutt=self.cmb_konuttipi.currentText()
        _cmb_isitma=self.cmb_isitma.currentText()
        _cmb_il=self.cmb_ilanil.currentText()
        _cwtarih=self.calendarWidget.selectedDate().toString(QtCore.Qt.ISODate)
        _spn_fiyat=self.spb_ilanfiyat.value()
        
        #check box seçim
        kredi_durumu="Uygun" if self.chckb_kredi.isChecked() else "-"
        satis="Satıldı" if self.chckb_satildi.isChecked() else "İlanda"
        
        #veri tabanı işlemleri
        try:
            self.curs.execute( 
                              "INSERT INTO emlak(TelNo, AdSoyad, Email, Ulasim, KonutT, Kat,"
                              " Alan, OdaS, Isıtma, BinaY, Fiyat ,Kredi, Il, Ilce, Adres,"
                               "Tarih,Satildi,EvDurumu) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                               (_lneTelno, _lneadSoyad, _lneemail, _cmb_ulasim,_cmb_konutt,_lne_kat, 
                                _lne_alan,_lne_odas,_cmb_isitma, _lne_binay, _spn_fiyat,
                                kredi_durumu,_cmb_il,_lne_ilce,_lne_adres,_cwtarih, satis, Ev_Durumu))
             
            self.conn.commit()
            QMessageBox.information(self,"BİLGİ","Kayıt Başarıyla Eklendi....")
        except sqlite3.Error as e:
            QMessageBox.critical(self,"Hata","Kayıt eklenirken hata: "+str(e))
                
        
           
    



    def baglanti_olustur(self):
        try:
            #veri tabanı oluştur
            self.conn=sqlite3.connect("veritabani.db")
            #kursör oluştur
            self.curs=self.conn.cursor()
            self.sorguCreTblEmlak=("CREATE TABLE IF NOT EXISTS Emlak( \
                                   id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,\
                                       TelNo TEXT NOT NULL UNIQUE, \
                                        AdSoyad TEXT NOT NULL,\
                                        Email TEXT NOT NULL,\
                                        Ulasim TEXT NOT NULL,\
                                        KonutT TEXT NOT NULL,\
                                        Kat TEXT NOT NULL,\
                                        Alan TEXT NOT NULL,\
                                        OdaS TEXT NOT NULL,\
                                        Isıtma TEXT NOT NULL,\
                                        BinaY TEXT NOT NULL,\
                                        Fiyat TEXT NOT NULL,\
                                        Kredi TEXT NOT NULL,\
                                        Il TEXT NOT NULL,\
                                        Ilce TEXT NOT NULL,\
                                        Adres TEXT NOT NULL,\
                                        Tarih TEXT NOT NULL,\
                                        Satildi TEXT NOT NULL,\
                                        EvDurumu TEXT NOT NULL)")
            
            #sorguyu çalıştır
            self.curs.execute(self.sorguCreTblEmlak)
            #veri tabanı değişikliklerini kaydet
            self.conn.commit()
            
        except sqlite3.Error as e:
            print("SQLite veritabanı Hatası: ",e)


            
                
    def listele(self):
        try:
            #tablo içeriğini temizlw
            self.tbl_liste.clear()
            self.tbl_liste.setRowCount(0)
            self.tbl_liste.setHorizontalHeaderLabels(('İlanNo','TelNo','Ad Soyad','E-Mail','Ulaşım',
                                                      'Konut Tipi','Kat','Alan','Oda+Salon','Isıtma',
                                                      'Bina Yaş','Fiyat','Kredi','İl','İlçe','Adres',
                                                       'Tarih','Satış Durumu','Ev Durumu'))
            self.tbl_liste.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            
            #veri tabanından tüm verileri al vetabloya ekle
            self.curs.execute("SELECT * FROM emlak")
            for satirIndeks,satirVeri in enumerate(self.curs):
                self.tbl_liste.insertRow(satirIndeks)
                for sutunIndeks, sutunVeri in enumerate(satirVeri):
                    self.tbl_liste.setItem(satirIndeks,sutunIndeks,QtWidgets.QTableWidgetItem(str(sutunVeri)))
                    
            #Giris alanlarını temizle
            self.lne_evshbad.clear()
            self.lne_evshbtelefon.clear()
            self.lne_evshbtelefon.setText("")
            self.lne_evshbmail.clear()
            self.lne_kat.clear()
            self.lne_alan.clear()
            self.lne_odasayisi.clear()
            self.lne_binaninyasi.clear()
            self.lne_ilanilce.clear()
            self.lne_adres.clear()
            self.cmb_evshbulasim.setCurrentIndex(-1)
            self.cmb_konuttipi.setCurrentIndex(-1)
            self.cmb_isitma.setCurrentIndex(-1)
            self.cmb_ilanil.setCurrentIndex(-1)
            self.spb_ilanfiyat.setValue(10000)
            self.rdb_kiralik.setChecked(False)
            self.rdb_satilik.setChecked(False)
            self.chckb_kredi.setChecked(False)
            self.chckb_satildi.setChecked(False)
            
            self.tbl_liste.setShowGrid(True)  #tablonun çizgileri
        
        except sqlite3.Error as e:
            print("SQLite Hatası: ", e)
    

    def kayit_sil(self):            
        cevap= QMessageBox.question(self, "KAYIT SİL","Kaydı silmek istiyor musunuz?",
                                    QMessageBox.Yes | QMessageBox.No)
        
        if cevap == QMessageBox.Yes:
            secili=self.tbl_liste.selectedItems()
            
            if secili:
                try:
                        silinecek=secili[1].text() #TelNo
                        self.statusbar.showMessage("Silinecek TelNo: " + silinecek, 10000)
                        
                        self.curs.execute("DELETE FROM emlak WHERE TelNo=?", (silinecek,))
                        self.conn.commit() 
                        self.listele()
                        self.statusbar.showMessage("Kayıt Başarıyla Silindi....",10000)
                        
                except sqlite3.Error as hata:
                    self.statusbar.showMessage("Hata Oluştu: "+ str(hata),10000)
                
  
            else:
                self.statusbar.showMessage("Silinecek Kaydı Seçin", 10000)
                
        else:
            self.statusbar.showMessage("Silme işlemi iptal Edildi!",10000 )
    
        
    def kayit_ara (self):
        a1 =self.lne_evshbtelefon.text() #telno
        a2 =self.lne_evshbmail.text()    #mail
        a3 =self.lne_evshbad.text()      #ad-soyad
        
        filtre= []
        if a1:
            filtre.append("TelNo = ?")
        if a2:
            filtre.append("Email = ?")
        if a3:
            filtre.append("AdSoyad = ?")
        
        fsorgu = " OR ".join(filtre)
        
        if fsorgu:
            sorgu =" SELECT * FROM emlak WHERE "+ fsorgu
            parametre = tuple(filter(lambda x: x, [a1,a2,a3]))
            
            self.curs.execute(sorgu, parametre)
            sonuc = self.curs.fetchall()
            
            self.tbl_liste.clearContents()
            self.tbl_liste.setRowCount(0) #satır sayısını sıfırla
            
            for satirIndeks, satirVeri in enumerate (sonuc):
                self.tbl_liste.insertRow(satirIndeks)
                for sutunIndeks, sutunVeri in enumerate (satirVeri):
                    self.tbl_liste.setItem(satirIndeks,sutunIndeks,QTableWidgetItem(str(sutunVeri)))
        else:            
            QMessageBox.warning(None,"Uyarı","Arama için en az bir kriter doldur.")
    
    def guncelle(self):
        cevap = QtWidgets.QMessageBox.question(self,"GÜNCELLE","Güncellemek istiyor musunuz? ",
                                             QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        
        if cevap == QtWidgets.QMessageBox.Yes:
            try:
                secili = self.tbl_liste.selectedItems()
                if secili:
                    _Id= int(secili[0].text())
                    _lneTelno=self.lne_evshbtelefon.text()
                    _lneadSoyad=self.lne_evshbad.text()
                    _lneemail=self.lne_evshbmail.text()
                    _lne_kat=self.lne_kat.text()
                    _lne_alan=self.lne_alan.text()
                    _lne_odas=self.lne_odasayisi.text()
                    _lne_binay=self.lne_binaninyasi.text()
                    _lne_ilce=self.lne_ilanilce.text()
                    _lne_adres=self.lne_adres.text()
                    
                    if not self.veri_giris_kontrol(_lneadSoyad,_lneTelno):
                        return
                    
                    if self.rdb_kiralik.isChecked():
                        Ev_Durumu="Kiralık"
                    elif self.rdb_satilik.isChecked():
                        Ev_Durumu="Satılık"
                    else:
                        Ev_Durumu="Belirtilmemiş"
        
                    _cmb_ulasim=self.cmb_evshbulasim.currentText()
                    _cmb_konutt=self.cmb_konuttipi.currentText()
                    _cmb_isitma=self.cmb_isitma.currentText()
                    _cmb_il=self.cmb_ilanil.currentText()
                    _cwtarih=self.calendarWidget.selectedDate().toString(QtCore.Qt.ISODate)
                    _spn_fiyat=self.spb_ilanfiyat.value()
                    
                    kredi_durumu="Uygun" if self.chckb_kredi.isChecked() else "-"
                    satis="Satıldı" if self.chckb_satildi.isChecked() else "İlanda"
                    
                    self.curs.execute(
                                    "UPDATE emlak SET TelNo=?, AdSoyad=?, Email=?, Ulasim=?, KonutT=?, Kat=?, Alan=?, OdaS=?, "
                                    "Isıtma=?, BinaY=?, Fiyat=?, Kredi=?, Il=?, Ilce=?, Adres=?, Tarih=?, Satildi=?, EvDurumu=? "
                                    "WHERE Id=?",
                                     (_lneTelno, _lneadSoyad, _lneemail, _cmb_ulasim, _cmb_konutt, _lne_kat, _lne_alan, _lne_odas,
                                     _cmb_isitma, _lne_binay, _spn_fiyat, kredi_durumu, _cmb_il, _lne_ilce, _lne_adres, _cwtarih,
                                     satis, Ev_Durumu, _Id))
                     
                    self.conn.commit()
                    self.listele()
                    self.statusBar().showMessage("Kayıt Güncellendi!",10000)
         
                else:
                    self.statusBar().showMessage("Kaydı Seçin!",10000)
            
            except sqlite3.Error as hata:
                self.statusBar().showMessage("Hata Oluştu: "+str(hata))
        
        else:
            self.statusbar.showMessage("Güncelleme işlemi iptal edildi",10000)
                        
    def doldur(self):               
        secili = self.tbl_liste.selectedItems()
        if len(secili) > 0:
            self.lne_evshbtelefon.setText(secili[1].text())
            self.lne_evshbad.setText(secili[2].text())
            self.lne_evshbmail.setText(secili[3].text())
            self.cmb_evshbulasim.setCurrentText(secili[4].text())
            self.cmb_konuttipi.setCurrentText(secili[5].text())
            self.lne_kat.setText(secili[6].text())
            self.lne_alan.setText(secili[7].text())
            self.lne_odasayisi.setText(secili[8].text())
            self.cmb_isitma.setCurrentText(secili[9].text())
            self.lne_binaninyasi.setText(secili[10].text())
            self.spb_ilanfiyat.setValue(int(secili[11].text()))
            
            kredi_durumu=secili[12].text()
            self.chckb_kredi.setChecked(kredi_durumu == "Uygun")
            
            self.cmb_ilanil.setCurrentText(secili[13].text())
            self.lne_ilanilce.setText(secili[14].text())
            self.lne_adres.setText(secili[15].text())
            
            tarih = secili[16].text()
            date=QtCore.QDate.fromString(tarih, QtCore.Qt.ISODate)
            self.calendarWidget.setSelectedDate(date)
            
            satis=secili[17].text()
            self.chckb_satildi.setChecked(satis == "Satıldı")
            
            #radio button için tek değişken
            evdurumu=secili[18].text()
            self.rdb_kiralik.setChecked(evdurumu == "Kiralık")
            self.rdb_satilik.setChecked(evdurumu == "Satılık")
        
        else:
            #Giris alanlarını temizle
            self.lne_evshbad.clear()
            self.lne_evshbtelefon.clear()
            self.lne_evshbtelefon.setText("")
            self.lne_evshbmail.clear()
            self.lne_kat.clear()
            self.lne_alan.clear()
            self.lne_odasayisi.clear()
            self.lne_binaninyasi.clear()
            self.lne_ilanilce.clear()
            self.lne_adres.clear()
            self.cmb_evshbulasim.setCurrentIndex(-1)
            self.cmb_konuttipi.setCurrentIndex(-1)
            self.cmb_isitma.setCurrentIndex(-1)
            self.cmb_ilanil.setCurrentIndex(-1)
            self.spb_ilanfiyat.setValue(10000)
            self.rdb_kiralik.setChecked(False)
            self.rdb_satilik.setChecked(False)
            self.chckb_kredi.setChecked(False)
            self.chckb_satildi.setChecked(False)
    
    def cikis(self):
     cevap = QMessageBox.question(self, "ÇIKIŞ", "Programdan çıkmak istiyor musunuz?",
                                  QMessageBox.Yes | QMessageBox.No)
     if cevap == QMessageBox.Yes:
         self.hakkinda_ve_cikis() #hakkında arayüzünü çalıştırmak için bağlantı
     else:
         self.statusBar().showMessage("Çıkış iptal edildi", 5000)
    
    #hakkında arayüzüyle ana programı birleştiren fonksiyon
    def hakkinda_ve_cikis(self):
        self.hakkinda_s = mw_hakkinda_class() #tanımlama
        self.hakkinda_s.show() #göster
        QtCore.QTimer.singleShot(3000, self.hakkinda_s.close)  # 3 saniye sonra kapat
        QtCore.QTimer.singleShot(3100, self.close)  # 3.1 saniye sonra ana pencereyi kapat
    
    #programı kapat
    def closeEvent(self, event): 
        self.conn.close()
        event.accept() #pencerenin kapatılmasını kabul et

        
if __name__=="__main__":
    import sys
    app=QtWidgets.QApplication(sys.argv)
    
    #programı şifregiriş arayüzüyle başlatma
    giris=mw_sifre_class() #tanımlama
    giris.show() #gösterme

    sys.exit(app.exec_())
