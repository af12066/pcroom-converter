#!/usr/bin/perl --

# pcroom-converter
#
# Copyright (c) 2016 T. H.
#
# This software is released under the MIT License.

# 実体参照変換
sub escape {
  my $str = $_[0];
  $str =~ s/&/&amp;/go;
  $str =~ s/</&lt;/go;
  $str =~ s/>/&gt;/go;
  $str =~ s/"/&quot;/go;
  $str =~ s/'/&#39;/go;
  return $str;
}

# 送信されたデータを受け取る
if ($ENV{'REQUEST_METHOD'} eq 'POST') {
  read(STDIN, $alldata, $ENV{'CONTENT_LENGTH'});
} else {
  $alldata = $ENV{'QUERY_STRING'};
}
foreach $data (split(/&/, $alldata)) {
  ($key, $value) = split(/=/, $data);
  # 送信されたデータの変換
  $value =~ s/\+/ /g;
  $value =~ s/　//g;
  $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack('C', hex($1))/eg;
  $value =~ s/\t//g;

  # 以下はフォームのパース
  # 全角スペースの有無は[　]*でないと厳しい
  if ($value =~ m/利用日.*：(.*)\n*/) {
   $date = $1;
  }
  if ($value =~ m/時[　]*限：(.*)\n*/) {
   $period = $1;
  }
  if ($value =~ m/利用者：(.*)\n*/) {
   $user = $1;
  }
  if ($value =~ m/目[　]*的：(.*)\n*/) {
   $object = $1;
  }
  if ($value =~ m/教[　]*室：(.*)\n*/) {
    $classroom = $1;
  }
  if ($classroom =~ /講義室/) {
    $classroom = "COLOR(#0000ff)" . $classroom;
  }
  if ($value =~ m/備[　]*考：(.*)\n*/) {
   $others = $1;
  }

  $output = "|" . $period . "|" . $classroom . "|" . $object . "|" . $user . "|" . $others . "|";
  $output =~ s/[\n\r]*//g;  # <pre>...</pre>に表示する際の改行文字削除
  $output = &escape($output);  # <pre>...</pre>内のエスケープ
  $in{"$key"} = $output;

  $escaped_date = &escape($date);  # 日付情報のエスケープ

}
print "Content-Type: text/html; charset=UTF-8\n\n";  # Header

print "<!DOCTYPE html>\n";
print "<html lang='ja'>\n";
print "<head>\n<meta charset='utf-8'>\n<link rel='stylesheet' href='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css' integrity='sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u' crossorigin='anonymous'>\n";  # Bootstrap CSS
print "<link rel='stylesheet' href='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css' integrity='sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp' crossorigin='anonymous'>\n";  # Bootstrap CSS (optional)
print "<title>臨時利用表作成ツール</title>\n";
print "</head>\n";
print "<body>\n";

print "<div class=\"container-fluid\">\n";
print "<div class=\"row\">\n";

print "<div class=\"col-sm-10 col-sm-offset-1\">\n";
print "<div class=\"page-header\">\n<h1>臨時利用表作成ツール</h1>\n</div>\n";
print "</div>\n";  # end col
print "</div>\n";  # end row

print "<div class=\"row\">\n";
print "<div class=\"col-sm-10 col-sm-offset-1\">\n";
print "<p>以下をWikiにコピペするのだ!</p>\n";
print "<strong>$escaped_dateの臨時利用:</strong>\n";  # Todo: 実体参照変換
print "<pre>$in{'message'}</pre>\n";
print "<br>\n";
print "<p><button type=\"button\" class=\"btn btn-default\" onclick=\"history.back()\">入力画面に戻る</button></p>\n";

print "</div>\n";  # end col
print "</div>\n";  # end row
print "</div>\n";  # end container
print "<script src='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js' integrity='sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa' crossorigin='anonymous'></script>\n";
print "</body>\n";
print "</html>\n";

exit;
