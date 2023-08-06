# Generated from grammar/SignalFlowV2Parser.g4 by ANTLR 4.5.2
# encoding: utf-8
from __future__ import print_function
from antlr4 import *
from io import StringIO

def serializedATN():
    with StringIO() as buf:
        buf.write(u"\3\u0430\ud6d1\u8206\uad2d\u4417\uaef1\u8d80\uaadd\3")
        buf.write(u"L\u025a\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t")
        buf.write(u"\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r")
        buf.write(u"\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4")
        buf.write(u"\23\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30")
        buf.write(u"\t\30\4\31\t\31\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t")
        buf.write(u"\35\4\36\t\36\4\37\t\37\4 \t \4!\t!\4\"\t\"\4#\t#\4$")
        buf.write(u"\t$\4%\t%\4&\t&\4\'\t\'\4(\t(\4)\t)\4*\t*\4+\t+\4,\t")
        buf.write(u",\4-\t-\4.\t.\4/\t/\4\60\t\60\4\61\t\61\4\62\t\62\4\63")
        buf.write(u"\t\63\4\64\t\64\4\65\t\65\4\66\t\66\4\67\t\67\48\t8\4")
        buf.write(u"9\t9\4:\t:\3\2\3\2\7\2w\n\2\f\2\16\2z\13\2\3\2\3\2\3")
        buf.write(u"\3\3\3\7\3\u0080\n\3\f\3\16\3\u0083\13\3\3\3\3\3\3\4")
        buf.write(u"\3\4\3\4\3\4\5\4\u008b\n\4\3\4\5\4\u008e\n\4\3\4\3\4")
        buf.write(u"\3\5\6\5\u0093\n\5\r\5\16\5\u0094\3\6\3\6\3\6\3\7\3\7")
        buf.write(u"\3\7\3\7\3\7\3\7\3\b\3\b\5\b\u00a2\n\b\3\b\3\b\3\t\3")
        buf.write(u"\t\3\t\7\t\u00a9\n\t\f\t\16\t\u00ac\13\t\3\t\3\t\3\t")
        buf.write(u"\3\t\5\t\u00b2\n\t\3\t\5\t\u00b5\n\t\5\t\u00b7\n\t\3")
        buf.write(u"\t\3\t\3\t\5\t\u00bc\n\t\3\t\5\t\u00bf\n\t\3\n\3\n\3")
        buf.write(u"\n\3\13\3\13\3\13\3\f\3\f\3\f\5\f\u00ca\n\f\3\r\3\r\3")
        buf.write(u"\16\3\16\5\16\u00d0\n\16\3\17\3\17\3\17\7\17\u00d5\n")
        buf.write(u"\17\f\17\16\17\u00d8\13\17\3\17\5\17\u00db\n\17\3\17")
        buf.write(u"\3\17\3\20\3\20\3\20\3\20\5\20\u00e3\n\20\3\21\3\21\3")
        buf.write(u"\21\5\21\u00e8\n\21\3\21\3\21\3\22\3\22\3\22\7\22\u00ef")
        buf.write(u"\n\22\f\22\16\22\u00f2\13\22\3\22\5\22\u00f5\n\22\3\23")
        buf.write(u"\3\23\5\23\u00f9\n\23\3\24\3\24\3\24\3\25\3\25\3\25\3")
        buf.write(u"\25\3\25\3\25\3\25\3\25\3\25\5\25\u0107\n\25\3\26\3\26")
        buf.write(u"\3\26\5\26\u010c\n\26\3\27\3\27\3\27\5\27\u0111\n\27")
        buf.write(u"\3\30\3\30\3\30\7\30\u0116\n\30\f\30\16\30\u0119\13\30")
        buf.write(u"\3\30\5\30\u011c\n\30\3\31\3\31\3\31\7\31\u0121\n\31")
        buf.write(u"\f\31\16\31\u0124\13\31\3\32\3\32\3\32\7\32\u0129\n\32")
        buf.write(u"\f\32\16\32\u012c\13\32\3\33\3\33\5\33\u0130\n\33\3\34")
        buf.write(u"\3\34\3\35\3\35\3\35\5\35\u0137\n\35\3\36\3\36\3\36\3")
        buf.write(u"\36\5\36\u013d\n\36\3\37\3\37\3\37\3\37\3\37\3\37\3\37")
        buf.write(u"\3\37\3\37\7\37\u0148\n\37\f\37\16\37\u014b\13\37\3\37")
        buf.write(u"\3\37\3\37\5\37\u0150\n\37\3 \3 \3 \3 \6 \u0156\n \r")
        buf.write(u" \16 \u0157\3 \3 \5 \u015c\n \3!\3!\3!\3!\3!\3!\5!\u0164")
        buf.write(u"\n!\3!\5!\u0167\n!\3\"\3\"\3\"\3\"\3\"\3#\3#\3#\7#\u0171")
        buf.write(u"\n#\f#\16#\u0174\13#\3$\3$\3$\7$\u0179\n$\f$\16$\u017c")
        buf.write(u"\13$\3%\3%\3%\5%\u0181\n%\3&\3&\3&\3&\3&\3&\3&\3&\3&")
        buf.write(u"\3&\3&\5&\u018e\n&\3&\7&\u0191\n&\f&\16&\u0194\13&\3")
        buf.write(u"\'\3\'\3\'\7\'\u0199\n\'\f\'\16\'\u019c\13\'\3(\3(\3")
        buf.write(u"(\7(\u01a1\n(\f(\16(\u01a4\13(\3)\3)\3)\7)\u01a9\n)\f")
        buf.write(u")\16)\u01ac\13)\3*\3*\3*\3*\3*\7*\u01b3\n*\f*\16*\u01b6")
        buf.write(u"\13*\3+\3+\3+\7+\u01bb\n+\f+\16+\u01be\13+\3,\3,\3,\7")
        buf.write(u",\u01c3\n,\f,\16,\u01c6\13,\3-\3-\3-\5-\u01cb\n-\3.\3")
        buf.write(u".\3.\5.\u01d0\n.\3/\3/\7/\u01d4\n/\f/\16/\u01d7\13/\3")
        buf.write(u"\60\3\60\3\60\3\60\3\60\3\60\3\60\6\60\u01e0\n\60\r\60")
        buf.write(u"\16\60\u01e1\3\60\3\60\3\60\5\60\u01e7\n\60\3\61\3\61")
        buf.write(u"\5\61\u01eb\n\61\3\61\3\61\3\61\3\61\3\61\3\61\3\61\5")
        buf.write(u"\61\u01f4\n\61\3\62\3\62\5\62\u01f8\n\62\3\62\3\62\5")
        buf.write(u"\62\u01fc\n\62\5\62\u01fe\n\62\3\63\3\63\3\63\3\63\7")
        buf.write(u"\63\u0204\n\63\f\63\16\63\u0207\13\63\5\63\u0209\n\63")
        buf.write(u"\3\63\3\63\3\64\3\64\5\64\u020f\n\64\3\64\3\64\3\65\3")
        buf.write(u"\65\3\65\3\65\3\65\3\65\3\65\3\65\3\65\7\65\u021c\n\65")
        buf.write(u"\f\65\16\65\u021f\13\65\3\65\5\65\u0222\n\65\5\65\u0224")
        buf.write(u"\n\65\3\65\3\65\3\66\3\66\3\66\7\66\u022b\n\66\f\66\16")
        buf.write(u"\66\u022e\13\66\3\66\5\66\u0231\n\66\3\67\3\67\3\67\7")
        buf.write(u"\67\u0236\n\67\f\67\16\67\u0239\13\67\3\67\3\67\5\67")
        buf.write(u"\u023d\n\67\3\67\3\67\3\67\7\67\u0242\n\67\f\67\16\67")
        buf.write(u"\u0245\13\67\3\67\3\67\5\67\u0249\n\67\3\67\5\67\u024c")
        buf.write(u"\n\67\38\38\38\39\39\39\3:\3:\5:\u0256\n:\3:\3:\3:\2")
        buf.write(u"\2;\2\4\6\b\n\f\16\20\22\24\26\30\32\34\36 \"$&(*,.\60")
        buf.write(u"\62\64\668:<>@BDFHJLNPRTVXZ\\^`bdfhjlnpr\2\6\3\3$$\3")
        buf.write(u"\2:;\4\2++<<\4\2:;==\u0281\2x\3\2\2\2\4}\3\2\2\2\6\u0086")
        buf.write(u"\3\2\2\2\b\u0092\3\2\2\2\n\u0096\3\2\2\2\f\u0099\3\2")
        buf.write(u"\2\2\16\u009f\3\2\2\2\20\u00be\3\2\2\2\22\u00c0\3\2\2")
        buf.write(u"\2\24\u00c3\3\2\2\2\26\u00c6\3\2\2\2\30\u00cb\3\2\2\2")
        buf.write(u"\32\u00cf\3\2\2\2\34\u00d1\3\2\2\2\36\u00e2\3\2\2\2 ")
        buf.write(u"\u00e7\3\2\2\2\"\u00eb\3\2\2\2$\u00f8\3\2\2\2&\u00fa")
        buf.write(u"\3\2\2\2(\u00fd\3\2\2\2*\u0108\3\2\2\2,\u010d\3\2\2\2")
        buf.write(u".\u0112\3\2\2\2\60\u011d\3\2\2\2\62\u0125\3\2\2\2\64")
        buf.write(u"\u012d\3\2\2\2\66\u0131\3\2\2\28\u0136\3\2\2\2:\u0138")
        buf.write(u"\3\2\2\2<\u013e\3\2\2\2>\u015b\3\2\2\2@\u0166\3\2\2\2")
        buf.write(u"B\u0168\3\2\2\2D\u016d\3\2\2\2F\u0175\3\2\2\2H\u0180")
        buf.write(u"\3\2\2\2J\u0182\3\2\2\2L\u0195\3\2\2\2N\u019d\3\2\2\2")
        buf.write(u"P\u01a5\3\2\2\2R\u01ad\3\2\2\2T\u01b7\3\2\2\2V\u01bf")
        buf.write(u"\3\2\2\2X\u01ca\3\2\2\2Z\u01cc\3\2\2\2\\\u01d1\3\2\2")
        buf.write(u"\2^\u01e6\3\2\2\2`\u01f3\3\2\2\2b\u01fd\3\2\2\2d\u01ff")
        buf.write(u"\3\2\2\2f\u020c\3\2\2\2h\u0212\3\2\2\2j\u0227\3\2\2\2")
        buf.write(u"l\u0237\3\2\2\2n\u024d\3\2\2\2p\u0250\3\2\2\2r\u0255")
        buf.write(u"\3\2\2\2tw\7$\2\2uw\5\32\16\2vt\3\2\2\2vu\3\2\2\2wz\3")
        buf.write(u"\2\2\2xv\3\2\2\2xy\3\2\2\2y{\3\2\2\2zx\3\2\2\2{|\7\2")
        buf.write(u"\2\3|\3\3\2\2\2}\u0081\5j\66\2~\u0080\7$\2\2\177~\3\2")
        buf.write(u"\2\2\u0080\u0083\3\2\2\2\u0081\177\3\2\2\2\u0081\u0082")
        buf.write(u"\3\2\2\2\u0082\u0084\3\2\2\2\u0083\u0081\3\2\2\2\u0084")
        buf.write(u"\u0085\7\2\2\3\u0085\5\3\2\2\2\u0086\u0087\7G\2\2\u0087")
        buf.write(u"\u008d\5\62\32\2\u0088\u008a\7,\2\2\u0089\u008b\5l\67")
        buf.write(u"\2\u008a\u0089\3\2\2\2\u008a\u008b\3\2\2\2\u008b\u008c")
        buf.write(u"\3\2\2\2\u008c\u008e\7-\2\2\u008d\u0088\3\2\2\2\u008d")
        buf.write(u"\u008e\3\2\2\2\u008e\u008f\3\2\2\2\u008f\u0090\7$\2\2")
        buf.write(u"\u0090\7\3\2\2\2\u0091\u0093\5\6\4\2\u0092\u0091\3\2")
        buf.write(u"\2\2\u0093\u0094\3\2\2\2\u0094\u0092\3\2\2\2\u0094\u0095")
        buf.write(u"\3\2\2\2\u0095\t\3\2\2\2\u0096\u0097\5\b\5\2\u0097\u0098")
        buf.write(u"\5\f\7\2\u0098\13\3\2\2\2\u0099\u009a\7\3\2\2\u009a\u009b")
        buf.write(u"\7%\2\2\u009b\u009c\5\16\b\2\u009c\u009d\7/\2\2\u009d")
        buf.write(u"\u009e\5> \2\u009e\r\3\2\2\2\u009f\u00a1\7,\2\2\u00a0")
        buf.write(u"\u00a2\5\20\t\2\u00a1\u00a0\3\2\2\2\u00a1\u00a2\3\2\2")
        buf.write(u"\2\u00a2\u00a3\3\2\2\2\u00a3\u00a4\7-\2\2\u00a4\17\3")
        buf.write(u"\2\2\2\u00a5\u00aa\5\26\f\2\u00a6\u00a7\7.\2\2\u00a7")
        buf.write(u"\u00a9\5\26\f\2\u00a8\u00a6\3\2\2\2\u00a9\u00ac\3\2\2")
        buf.write(u"\2\u00aa\u00a8\3\2\2\2\u00aa\u00ab\3\2\2\2\u00ab\u00b6")
        buf.write(u"\3\2\2\2\u00ac\u00aa\3\2\2\2\u00ad\u00b4\7.\2\2\u00ae")
        buf.write(u"\u00b1\5\22\n\2\u00af\u00b0\7.\2\2\u00b0\u00b2\5\24\13")
        buf.write(u"\2\u00b1\u00af\3\2\2\2\u00b1\u00b2\3\2\2\2\u00b2\u00b5")
        buf.write(u"\3\2\2\2\u00b3\u00b5\5\24\13\2\u00b4\u00ae\3\2\2\2\u00b4")
        buf.write(u"\u00b3\3\2\2\2\u00b4\u00b5\3\2\2\2\u00b5\u00b7\3\2\2")
        buf.write(u"\2\u00b6\u00ad\3\2\2\2\u00b6\u00b7\3\2\2\2\u00b7\u00bf")
        buf.write(u"\3\2\2\2\u00b8\u00bb\5\22\n\2\u00b9\u00ba\7.\2\2\u00ba")
        buf.write(u"\u00bc\5\24\13\2\u00bb\u00b9\3\2\2\2\u00bb\u00bc\3\2")
        buf.write(u"\2\2\u00bc\u00bf\3\2\2\2\u00bd\u00bf\5\24\13\2\u00be")
        buf.write(u"\u00a5\3\2\2\2\u00be\u00b8\3\2\2\2\u00be\u00bd\3\2\2")
        buf.write(u"\2\u00bf\21\3\2\2\2\u00c0\u00c1\7+\2\2\u00c1\u00c2\5")
        buf.write(u"\30\r\2\u00c2\23\3\2\2\2\u00c3\u00c4\7\61\2\2\u00c4\u00c5")
        buf.write(u"\5\30\r\2\u00c5\25\3\2\2\2\u00c6\u00c9\5\30\r\2\u00c7")
        buf.write(u"\u00c8\7\62\2\2\u00c8\u00ca\5@!\2\u00c9\u00c7\3\2\2\2")
        buf.write(u"\u00c9\u00ca\3\2\2\2\u00ca\27\3\2\2\2\u00cb\u00cc\7%")
        buf.write(u"\2\2\u00cc\31\3\2\2\2\u00cd\u00d0\5\34\17\2\u00ce\u00d0")
        buf.write(u"\58\35\2\u00cf\u00cd\3\2\2\2\u00cf\u00ce\3\2\2\2\u00d0")
        buf.write(u"\33\3\2\2\2\u00d1\u00d6\5\36\20\2\u00d2\u00d3\7\60\2")
        buf.write(u"\2\u00d3\u00d5\5\36\20\2\u00d4\u00d2\3\2\2\2\u00d5\u00d8")
        buf.write(u"\3\2\2\2\u00d6\u00d4\3\2\2\2\u00d6\u00d7\3\2\2\2\u00d7")
        buf.write(u"\u00da\3\2\2\2\u00d8\u00d6\3\2\2\2\u00d9\u00db\7\60\2")
        buf.write(u"\2\u00da\u00d9\3\2\2\2\u00da\u00db\3\2\2\2\u00db\u00dc")
        buf.write(u"\3\2\2\2\u00dc\u00dd\t\2\2\2\u00dd\35\3\2\2\2\u00de\u00e3")
        buf.write(u"\5 \21\2\u00df\u00e3\5\66\34\2\u00e0\u00e3\5$\23\2\u00e1")
        buf.write(u"\u00e3\5:\36\2\u00e2\u00de\3\2\2\2\u00e2\u00df\3\2\2")
        buf.write(u"\2\u00e2\u00e0\3\2\2\2\u00e2\u00e1\3\2\2\2\u00e3\37\3")
        buf.write(u"\2\2\2\u00e4\u00e5\5\"\22\2\u00e5\u00e6\7\62\2\2\u00e6")
        buf.write(u"\u00e8\3\2\2\2\u00e7\u00e4\3\2\2\2\u00e7\u00e8\3\2\2")
        buf.write(u"\2\u00e8\u00e9\3\2\2\2\u00e9\u00ea\5j\66\2\u00ea!\3\2")
        buf.write(u"\2\2\u00eb\u00f0\7%\2\2\u00ec\u00ed\7.\2\2\u00ed\u00ef")
        buf.write(u"\7%\2\2\u00ee\u00ec\3\2\2\2\u00ef\u00f2\3\2\2\2\u00f0")
        buf.write(u"\u00ee\3\2\2\2\u00f0\u00f1\3\2\2\2\u00f1\u00f4\3\2\2")
        buf.write(u"\2\u00f2\u00f0\3\2\2\2\u00f3\u00f5\7.\2\2\u00f4\u00f3")
        buf.write(u"\3\2\2\2\u00f4\u00f5\3\2\2\2\u00f5#\3\2\2\2\u00f6\u00f9")
        buf.write(u"\5&\24\2\u00f7\u00f9\5(\25\2\u00f8\u00f6\3\2\2\2\u00f8")
        buf.write(u"\u00f7\3\2\2\2\u00f9%\3\2\2\2\u00fa\u00fb\7\7\2\2\u00fb")
        buf.write(u"\u00fc\5\60\31\2\u00fc\'\3\2\2\2\u00fd\u00fe\7\6\2\2")
        buf.write(u"\u00fe\u00ff\5\62\32\2\u00ff\u0106\7\7\2\2\u0100\u0107")
        buf.write(u"\7+\2\2\u0101\u0102\7,\2\2\u0102\u0103\5.\30\2\u0103")
        buf.write(u"\u0104\7-\2\2\u0104\u0107\3\2\2\2\u0105\u0107\5.\30\2")
        buf.write(u"\u0106\u0100\3\2\2\2\u0106\u0101\3\2\2\2\u0106\u0105")
        buf.write(u"\3\2\2\2\u0107)\3\2\2\2\u0108\u010b\7%\2\2\u0109\u010a")
        buf.write(u"\7\b\2\2\u010a\u010c\7%\2\2\u010b\u0109\3\2\2\2\u010b")
        buf.write(u"\u010c\3\2\2\2\u010c+\3\2\2\2\u010d\u0110\5\62\32\2\u010e")
        buf.write(u"\u010f\7\b\2\2\u010f\u0111\7%\2\2\u0110\u010e\3\2\2\2")
        buf.write(u"\u0110\u0111\3\2\2\2\u0111-\3\2\2\2\u0112\u0117\5*\26")
        buf.write(u"\2\u0113\u0114\7.\2\2\u0114\u0116\5*\26\2\u0115\u0113")
        buf.write(u"\3\2\2\2\u0116\u0119\3\2\2\2\u0117\u0115\3\2\2\2\u0117")
        buf.write(u"\u0118\3\2\2\2\u0118\u011b\3\2\2\2\u0119\u0117\3\2\2")
        buf.write(u"\2\u011a\u011c\7.\2\2\u011b\u011a\3\2\2\2\u011b\u011c")
        buf.write(u"\3\2\2\2\u011c/\3\2\2\2\u011d\u0122\5,\27\2\u011e\u011f")
        buf.write(u"\7.\2\2\u011f\u0121\5,\27\2\u0120\u011e\3\2\2\2\u0121")
        buf.write(u"\u0124\3\2\2\2\u0122\u0120\3\2\2\2\u0122\u0123\3\2\2")
        buf.write(u"\2\u0123\61\3\2\2\2\u0124\u0122\3\2\2\2\u0125\u012a\7")
        buf.write(u"%\2\2\u0126\u0127\7)\2\2\u0127\u0129\7%\2\2\u0128\u0126")
        buf.write(u"\3\2\2\2\u0129\u012c\3\2\2\2\u012a\u0128\3\2\2\2\u012a")
        buf.write(u"\u012b\3\2\2\2\u012b\63\3\2\2\2\u012c\u012a\3\2\2\2\u012d")
        buf.write(u"\u012f\7\4\2\2\u012e\u0130\5j\66\2\u012f\u012e\3\2\2")
        buf.write(u"\2\u012f\u0130\3\2\2\2\u0130\65\3\2\2\2\u0131\u0132\5")
        buf.write(u"\64\33\2\u0132\67\3\2\2\2\u0133\u0137\5<\37\2\u0134\u0137")
        buf.write(u"\5\f\7\2\u0135\u0137\5\n\6\2\u0136\u0133\3\2\2\2\u0136")
        buf.write(u"\u0134\3\2\2\2\u0136\u0135\3\2\2\2\u01379\3\2\2\2\u0138")
        buf.write(u"\u0139\7\13\2\2\u0139\u013c\5@!\2\u013a\u013b\7.\2\2")
        buf.write(u"\u013b\u013d\5@!\2\u013c\u013a\3\2\2\2\u013c\u013d\3")
        buf.write(u"\2\2\2\u013d;\3\2\2\2\u013e\u013f\7\f\2\2\u013f\u0140")
        buf.write(u"\5@!\2\u0140\u0141\7/\2\2\u0141\u0149\5> \2\u0142\u0143")
        buf.write(u"\7\r\2\2\u0143\u0144\5@!\2\u0144\u0145\7/\2\2\u0145\u0146")
        buf.write(u"\5> \2\u0146\u0148\3\2\2\2\u0147\u0142\3\2\2\2\u0148")
        buf.write(u"\u014b\3\2\2\2\u0149\u0147\3\2\2\2\u0149\u014a\3\2\2")
        buf.write(u"\2\u014a\u014f\3\2\2\2\u014b\u0149\3\2\2\2\u014c\u014d")
        buf.write(u"\7\16\2\2\u014d\u014e\7/\2\2\u014e\u0150\5> \2\u014f")
        buf.write(u"\u014c\3\2\2\2\u014f\u0150\3\2\2\2\u0150=\3\2\2\2\u0151")
        buf.write(u"\u015c\5\34\17\2\u0152\u0153\7$\2\2\u0153\u0155\7K\2")
        buf.write(u"\2\u0154\u0156\5\32\16\2\u0155\u0154\3\2\2\2\u0156\u0157")
        buf.write(u"\3\2\2\2\u0157\u0155\3\2\2\2\u0157\u0158\3\2\2\2\u0158")
        buf.write(u"\u0159\3\2\2\2\u0159\u015a\7L\2\2\u015a\u015c\3\2\2\2")
        buf.write(u"\u015b\u0151\3\2\2\2\u015b\u0152\3\2\2\2\u015c?\3\2\2")
        buf.write(u"\2\u015d\u0163\5D#\2\u015e\u015f\7\f\2\2\u015f\u0160")
        buf.write(u"\5D#\2\u0160\u0161\7\16\2\2\u0161\u0162\5@!\2\u0162\u0164")
        buf.write(u"\3\2\2\2\u0163\u015e\3\2\2\2\u0163\u0164\3\2\2\2\u0164")
        buf.write(u"\u0167\3\2\2\2\u0165\u0167\5B\"\2\u0166\u015d\3\2\2\2")
        buf.write(u"\u0166\u0165\3\2\2\2\u0167A\3\2\2\2\u0168\u0169\7\26")
        buf.write(u"\2\2\u0169\u016a\7%\2\2\u016a\u016b\7/\2\2\u016b\u016c")
        buf.write(u"\5@!\2\u016cC\3\2\2\2\u016d\u0172\5F$\2\u016e\u016f\7")
        buf.write(u"\27\2\2\u016f\u0171\5F$\2\u0170\u016e\3\2\2\2\u0171\u0174")
        buf.write(u"\3\2\2\2\u0172\u0170\3\2\2\2\u0172\u0173\3\2\2\2\u0173")
        buf.write(u"E\3\2\2\2\u0174\u0172\3\2\2\2\u0175\u017a\5H%\2\u0176")
        buf.write(u"\u0177\7\30\2\2\u0177\u0179\5H%\2\u0178\u0176\3\2\2\2")
        buf.write(u"\u0179\u017c\3\2\2\2\u017a\u0178\3\2\2\2\u017a\u017b")
        buf.write(u"\3\2\2\2\u017bG\3\2\2\2\u017c\u017a\3\2\2\2\u017d\u017e")
        buf.write(u"\7\31\2\2\u017e\u0181\5H%\2\u017f\u0181\5J&\2\u0180\u017d")
        buf.write(u"\3\2\2\2\u0180\u017f\3\2\2\2\u0181I\3\2\2\2\u0182\u0192")
        buf.write(u"\5L\'\2\u0183\u018e\7@\2\2\u0184\u018e\7D\2\2\u0185\u018e")
        buf.write(u"\7B\2\2\u0186\u018e\7E\2\2\u0187\u018e\7F\2\2\u0188\u018e")
        buf.write(u"\7A\2\2\u0189\u018e\7C\2\2\u018a\u018e\7\32\2\2\u018b")
        buf.write(u"\u018c\7\32\2\2\u018c\u018e\7\31\2\2\u018d\u0183\3\2")
        buf.write(u"\2\2\u018d\u0184\3\2\2\2\u018d\u0185\3\2\2\2\u018d\u0186")
        buf.write(u"\3\2\2\2\u018d\u0187\3\2\2\2\u018d\u0188\3\2\2\2\u018d")
        buf.write(u"\u0189\3\2\2\2\u018d\u018a\3\2\2\2\u018d\u018b\3\2\2")
        buf.write(u"\2\u018e\u018f\3\2\2\2\u018f\u0191\5L\'\2\u0190\u018d")
        buf.write(u"\3\2\2\2\u0191\u0194\3\2\2\2\u0192\u0190\3\2\2\2\u0192")
        buf.write(u"\u0193\3\2\2\2\u0193K\3\2\2\2\u0194\u0192\3\2\2\2\u0195")
        buf.write(u"\u019a\5N(\2\u0196\u0197\7\65\2\2\u0197\u0199\5N(\2\u0198")
        buf.write(u"\u0196\3\2\2\2\u0199\u019c\3\2\2\2\u019a\u0198\3\2\2")
        buf.write(u"\2\u019a\u019b\3\2\2\2\u019bM\3\2\2\2\u019c\u019a\3\2")
        buf.write(u"\2\2\u019d\u01a2\5P)\2\u019e\u019f\7\66\2\2\u019f\u01a1")
        buf.write(u"\5P)\2\u01a0\u019e\3\2\2\2\u01a1\u01a4\3\2\2\2\u01a2")
        buf.write(u"\u01a0\3\2\2\2\u01a2\u01a3\3\2\2\2\u01a3O\3\2\2\2\u01a4")
        buf.write(u"\u01a2\3\2\2\2\u01a5\u01aa\5R*\2\u01a6\u01a7\7\67\2\2")
        buf.write(u"\u01a7\u01a9\5R*\2\u01a8\u01a6\3\2\2\2\u01a9\u01ac\3")
        buf.write(u"\2\2\2\u01aa\u01a8\3\2\2\2\u01aa\u01ab\3\2\2\2\u01ab")
        buf.write(u"Q\3\2\2\2\u01ac\u01aa\3\2\2\2\u01ad\u01b4\5T+\2\u01ae")
        buf.write(u"\u01af\78\2\2\u01af\u01b3\5T+\2\u01b0\u01b1\79\2\2\u01b1")
        buf.write(u"\u01b3\5T+\2\u01b2\u01ae\3\2\2\2\u01b2\u01b0\3\2\2\2")
        buf.write(u"\u01b3\u01b6\3\2\2\2\u01b4\u01b2\3\2\2\2\u01b4\u01b5")
        buf.write(u"\3\2\2\2\u01b5S\3\2\2\2\u01b6\u01b4\3\2\2\2\u01b7\u01bc")
        buf.write(u"\5V,\2\u01b8\u01b9\t\3\2\2\u01b9\u01bb\5V,\2\u01ba\u01b8")
        buf.write(u"\3\2\2\2\u01bb\u01be\3\2\2\2\u01bc\u01ba\3\2\2\2\u01bc")
        buf.write(u"\u01bd\3\2\2\2\u01bdU\3\2\2\2\u01be\u01bc\3\2\2\2\u01bf")
        buf.write(u"\u01c4\5X-\2\u01c0\u01c1\t\4\2\2\u01c1\u01c3\5X-\2\u01c2")
        buf.write(u"\u01c0\3\2\2\2\u01c3\u01c6\3\2\2\2\u01c4\u01c2\3\2\2")
        buf.write(u"\2\u01c4\u01c5\3\2\2\2\u01c5W\3\2\2\2\u01c6\u01c4\3\2")
        buf.write(u"\2\2\u01c7\u01c8\t\5\2\2\u01c8\u01cb\5X-\2\u01c9\u01cb")
        buf.write(u"\5Z.\2\u01ca\u01c7\3\2\2\2\u01ca\u01c9\3\2\2\2\u01cb")
        buf.write(u"Y\3\2\2\2\u01cc\u01cf\5\\/\2\u01cd\u01ce\7\61\2\2\u01ce")
        buf.write(u"\u01d0\5X-\2\u01cf\u01cd\3\2\2\2\u01cf\u01d0\3\2\2\2")
        buf.write(u"\u01d0[\3\2\2\2\u01d1\u01d5\5^\60\2\u01d2\u01d4\5`\61")
        buf.write(u"\2\u01d3\u01d2\3\2\2\2\u01d4\u01d7\3\2\2\2\u01d5\u01d3")
        buf.write(u"\3\2\2\2\u01d5\u01d6\3\2\2\2\u01d6]\3\2\2\2\u01d7\u01d5")
        buf.write(u"\3\2\2\2\u01d8\u01e7\5d\63\2\u01d9\u01e7\5f\64\2\u01da")
        buf.write(u"\u01e7\5h\65\2\u01db\u01e7\7%\2\2\u01dc\u01e7\7\'\2\2")
        buf.write(u"\u01dd\u01e7\7(\2\2\u01de\u01e0\7&\2\2\u01df\u01de\3")
        buf.write(u"\2\2\2\u01e0\u01e1\3\2\2\2\u01e1\u01df\3\2\2\2\u01e1")
        buf.write(u"\u01e2\3\2\2\2\u01e2\u01e7\3\2\2\2\u01e3\u01e7\7\33\2")
        buf.write(u"\2\u01e4\u01e7\7\34\2\2\u01e5\u01e7\7\35\2\2\u01e6\u01d8")
        buf.write(u"\3\2\2\2\u01e6\u01d9\3\2\2\2\u01e6\u01da\3\2\2\2\u01e6")
        buf.write(u"\u01db\3\2\2\2\u01e6\u01dc\3\2\2\2\u01e6\u01dd\3\2\2")
        buf.write(u"\2\u01e6\u01df\3\2\2\2\u01e6\u01e3\3\2\2\2\u01e6\u01e4")
        buf.write(u"\3\2\2\2\u01e6\u01e5\3\2\2\2\u01e7_\3\2\2\2\u01e8\u01ea")
        buf.write(u"\7,\2\2\u01e9\u01eb\5l\67\2\u01ea\u01e9\3\2\2\2\u01ea")
        buf.write(u"\u01eb\3\2\2\2\u01eb\u01ec\3\2\2\2\u01ec\u01f4\7-\2\2")
        buf.write(u"\u01ed\u01ee\7\63\2\2\u01ee\u01ef\5b\62\2\u01ef\u01f0")
        buf.write(u"\7\64\2\2\u01f0\u01f4\3\2\2\2\u01f1\u01f2\7)\2\2\u01f2")
        buf.write(u"\u01f4\7%\2\2\u01f3\u01e8\3\2\2\2\u01f3\u01ed\3\2\2\2")
        buf.write(u"\u01f3\u01f1\3\2\2\2\u01f4a\3\2\2\2\u01f5\u01fe\5@!\2")
        buf.write(u"\u01f6\u01f8\5@!\2\u01f7\u01f6\3\2\2\2\u01f7\u01f8\3")
        buf.write(u"\2\2\2\u01f8\u01f9\3\2\2\2\u01f9\u01fb\7/\2\2\u01fa\u01fc")
        buf.write(u"\5@!\2\u01fb\u01fa\3\2\2\2\u01fb\u01fc\3\2\2\2\u01fc")
        buf.write(u"\u01fe\3\2\2\2\u01fd\u01f5\3\2\2\2\u01fd\u01f7\3\2\2")
        buf.write(u"\2\u01fec\3\2\2\2\u01ff\u0208\7\63\2\2\u0200\u0205\5")
        buf.write(u"@!\2\u0201\u0202\7.\2\2\u0202\u0204\5@!\2\u0203\u0201")
        buf.write(u"\3\2\2\2\u0204\u0207\3\2\2\2\u0205\u0203\3\2\2\2\u0205")
        buf.write(u"\u0206\3\2\2\2\u0206\u0209\3\2\2\2\u0207\u0205\3\2\2")
        buf.write(u"\2\u0208\u0200\3\2\2\2\u0208\u0209\3\2\2\2\u0209\u020a")
        buf.write(u"\3\2\2\2\u020a\u020b\7\64\2\2\u020be\3\2\2\2\u020c\u020e")
        buf.write(u"\7,\2\2\u020d\u020f\5j\66\2\u020e\u020d\3\2\2\2\u020e")
        buf.write(u"\u020f\3\2\2\2\u020f\u0210\3\2\2\2\u0210\u0211\7-\2\2")
        buf.write(u"\u0211g\3\2\2\2\u0212\u0223\7>\2\2\u0213\u0214\5@!\2")
        buf.write(u"\u0214\u0215\7/\2\2\u0215\u021d\5@!\2\u0216\u0217\7.")
        buf.write(u"\2\2\u0217\u0218\5@!\2\u0218\u0219\7/\2\2\u0219\u021a")
        buf.write(u"\5@!\2\u021a\u021c\3\2\2\2\u021b\u0216\3\2\2\2\u021c")
        buf.write(u"\u021f\3\2\2\2\u021d\u021b\3\2\2\2\u021d\u021e\3\2\2")
        buf.write(u"\2\u021e\u0221\3\2\2\2\u021f\u021d\3\2\2\2\u0220\u0222")
        buf.write(u"\7.\2\2\u0221\u0220\3\2\2\2\u0221\u0222\3\2\2\2\u0222")
        buf.write(u"\u0224\3\2\2\2\u0223\u0213\3\2\2\2\u0223\u0224\3\2\2")
        buf.write(u"\2\u0224\u0225\3\2\2\2\u0225\u0226\7?\2\2\u0226i\3\2")
        buf.write(u"\2\2\u0227\u022c\5@!\2\u0228\u0229\7.\2\2\u0229\u022b")
        buf.write(u"\5@!\2\u022a\u0228\3\2\2\2\u022b\u022e\3\2\2\2\u022c")
        buf.write(u"\u022a\3\2\2\2\u022c\u022d\3\2\2\2\u022d\u0230\3\2\2")
        buf.write(u"\2\u022e\u022c\3\2\2\2\u022f\u0231\7.\2\2\u0230\u022f")
        buf.write(u"\3\2\2\2\u0230\u0231\3\2\2\2\u0231k\3\2\2\2\u0232\u0233")
        buf.write(u"\5r:\2\u0233\u0234\7.\2\2\u0234\u0236\3\2\2\2\u0235\u0232")
        buf.write(u"\3\2\2\2\u0236\u0239\3\2\2\2\u0237\u0235\3\2\2\2\u0237")
        buf.write(u"\u0238\3\2\2\2\u0238\u024b\3\2\2\2\u0239\u0237\3\2\2")
        buf.write(u"\2\u023a\u023c\5r:\2\u023b\u023d\7.\2\2\u023c\u023b\3")
        buf.write(u"\2\2\2\u023c\u023d\3\2\2\2\u023d\u024c\3\2\2\2\u023e")
        buf.write(u"\u0243\5n8\2\u023f\u0240\7.\2\2\u0240\u0242\5r:\2\u0241")
        buf.write(u"\u023f\3\2\2\2\u0242\u0245\3\2\2\2\u0243\u0241\3\2\2")
        buf.write(u"\2\u0243\u0244\3\2\2\2\u0244\u0248\3\2\2\2\u0245\u0243")
        buf.write(u"\3\2\2\2\u0246\u0247\7.\2\2\u0247\u0249\5p9\2\u0248\u0246")
        buf.write(u"\3\2\2\2\u0248\u0249\3\2\2\2\u0249\u024c\3\2\2\2\u024a")
        buf.write(u"\u024c\5p9\2\u024b\u023a\3\2\2\2\u024b\u023e\3\2\2\2")
        buf.write(u"\u024b\u024a\3\2\2\2\u024cm\3\2\2\2\u024d\u024e\7+\2")
        buf.write(u"\2\u024e\u024f\5@!\2\u024fo\3\2\2\2\u0250\u0251\7\61")
        buf.write(u"\2\2\u0251\u0252\5@!\2\u0252q\3\2\2\2\u0253\u0254\7%")
        buf.write(u"\2\2\u0254\u0256\7\62\2\2\u0255\u0253\3\2\2\2\u0255\u0256")
        buf.write(u"\3\2\2\2\u0256\u0257\3\2\2\2\u0257\u0258\5@!\2\u0258")
        buf.write(u"s\3\2\2\2Lvx\u0081\u008a\u008d\u0094\u00a1\u00aa\u00b1")
        buf.write(u"\u00b4\u00b6\u00bb\u00be\u00c9\u00cf\u00d6\u00da\u00e2")
        buf.write(u"\u00e7\u00f0\u00f4\u00f8\u0106\u010b\u0110\u0117\u011b")
        buf.write(u"\u0122\u012a\u012f\u0136\u013c\u0149\u014f\u0157\u015b")
        buf.write(u"\u0163\u0166\u0172\u017a\u0180\u018d\u0192\u019a\u01a2")
        buf.write(u"\u01aa\u01b2\u01b4\u01bc\u01c4\u01ca\u01cf\u01d5\u01e1")
        buf.write(u"\u01e6\u01ea\u01f3\u01f7\u01fb\u01fd\u0205\u0208\u020e")
        buf.write(u"\u021d\u0221\u0223\u022c\u0230\u0237\u023c\u0243\u0248")
        buf.write(u"\u024b\u0255")
        return buf.getvalue()


class SignalFlowV2Parser ( Parser ):

    grammarFileName = "SignalFlowV2Parser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ u"<INVALID>", u"'def'", u"'return'", u"'raise'", u"'from'", 
                     u"'import'", u"'as'", u"'global'", u"'nonlocal'", u"'assert'", 
                     u"'if'", u"'elif'", u"'else'", u"'while'", u"'for'", 
                     u"'in'", u"'try'", u"'finally'", u"'with'", u"'except'", 
                     u"'lambda'", u"'or'", u"'and'", u"'not'", u"'is'", 
                     u"'None'", u"'True'", u"'False'", u"'class'", u"'yield'", 
                     u"'del'", u"'pass'", u"'continue'", u"'break'", u"<INVALID>", 
                     u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>", 
                     u"'.'", u"'...'", u"'*'", u"'('", u"')'", u"','", u"':'", 
                     u"';'", u"'**'", u"'='", u"'['", u"']'", u"'|'", u"'^'", 
                     u"'&'", u"'<<'", u"'>>'", u"'+'", u"'-'", u"'/'", u"'~'", 
                     u"'{'", u"'}'", u"'<'", u"'>'", u"'=='", u"'>='", u"'<='", 
                     u"'<>'", u"'!='", u"'@'", u"'->'" ]

    symbolicNames = [ u"<INVALID>", u"DEF", u"RETURN", u"RAISE", u"FROM", 
                      u"IMPORT", u"AS", u"GLOBAL", u"NONLOCAL", u"ASSERT", 
                      u"IF", u"ELIF", u"ELSE", u"WHILE", u"FOR", u"IN", 
                      u"TRY", u"FINALLY", u"WITH", u"EXCEPT", u"LAMBDA", 
                      u"OR", u"AND", u"NOT", u"IS", u"NONE", u"TRUE", u"FALSE", 
                      u"CLASS", u"YIELD", u"DEL", u"PASS", u"CONTINUE", 
                      u"BREAK", u"NEWLINE", u"ID", u"STRING", u"INT", u"FLOAT", 
                      u"DOT", u"ELLIPSE", u"STAR", u"OPEN_PAREN", u"CLOSE_PAREN", 
                      u"COMMA", u"COLON", u"SEMICOLON", u"POWER", u"ASSIGN", 
                      u"OPEN_BRACK", u"CLOSE_BRACK", u"OR_OP", u"XOR", u"AND_OP", 
                      u"LEFT_SHIFT", u"RIGHT_SHIFT", u"ADD", u"MINUS", u"DIV", 
                      u"NOT_OP", u"OPEN_BRACE", u"CLOSE_BRACE", u"LESS_THAN", 
                      u"GREATER_THAN", u"EQUALS", u"GT_EQ", u"LT_EQ", u"NOT_EQ_1", 
                      u"NOT_EQ_2", u"AT", u"ARROW", u"SKIP_", u"COMMENT", 
                      u"INDENT", u"DEDENT" ]

    RULE_program = 0
    RULE_eval_input = 1
    RULE_decorator = 2
    RULE_decorators = 3
    RULE_decorated = 4
    RULE_function_definition = 5
    RULE_parameters = 6
    RULE_var_args_list = 7
    RULE_var_args_star_param = 8
    RULE_var_args_kws_param = 9
    RULE_var_args_list_param_def = 10
    RULE_var_args_list_param_name = 11
    RULE_statement = 12
    RULE_simple_statement = 13
    RULE_small_statement = 14
    RULE_expr_statement = 15
    RULE_id_list = 16
    RULE_import_statement = 17
    RULE_import_name = 18
    RULE_import_from = 19
    RULE_import_as_name = 20
    RULE_dotted_as_name = 21
    RULE_import_as_names = 22
    RULE_dotted_as_names = 23
    RULE_dotted_name = 24
    RULE_return_statement = 25
    RULE_flow_statement = 26
    RULE_compound_statement = 27
    RULE_assert_statement = 28
    RULE_if_statement = 29
    RULE_suite = 30
    RULE_test = 31
    RULE_lambdef = 32
    RULE_or_test = 33
    RULE_and_test = 34
    RULE_not_test = 35
    RULE_comparison = 36
    RULE_expr = 37
    RULE_xor_expr = 38
    RULE_and_expr = 39
    RULE_shift_expr = 40
    RULE_arith_expr = 41
    RULE_term = 42
    RULE_factor = 43
    RULE_power = 44
    RULE_atom_expr = 45
    RULE_atom = 46
    RULE_trailer = 47
    RULE_subscript = 48
    RULE_list_expr = 49
    RULE_tuple_expr = 50
    RULE_dict_expr = 51
    RULE_testlist = 52
    RULE_actual_args = 53
    RULE_actual_star_arg = 54
    RULE_actual_kws_arg = 55
    RULE_argument = 56

    ruleNames =  [ u"program", u"eval_input", u"decorator", u"decorators", 
                   u"decorated", u"function_definition", u"parameters", 
                   u"var_args_list", u"var_args_star_param", u"var_args_kws_param", 
                   u"var_args_list_param_def", u"var_args_list_param_name", 
                   u"statement", u"simple_statement", u"small_statement", 
                   u"expr_statement", u"id_list", u"import_statement", u"import_name", 
                   u"import_from", u"import_as_name", u"dotted_as_name", 
                   u"import_as_names", u"dotted_as_names", u"dotted_name", 
                   u"return_statement", u"flow_statement", u"compound_statement", 
                   u"assert_statement", u"if_statement", u"suite", u"test", 
                   u"lambdef", u"or_test", u"and_test", u"not_test", u"comparison", 
                   u"expr", u"xor_expr", u"and_expr", u"shift_expr", u"arith_expr", 
                   u"term", u"factor", u"power", u"atom_expr", u"atom", 
                   u"trailer", u"subscript", u"list_expr", u"tuple_expr", 
                   u"dict_expr", u"testlist", u"actual_args", u"actual_star_arg", 
                   u"actual_kws_arg", u"argument" ]

    EOF = Token.EOF
    DEF=1
    RETURN=2
    RAISE=3
    FROM=4
    IMPORT=5
    AS=6
    GLOBAL=7
    NONLOCAL=8
    ASSERT=9
    IF=10
    ELIF=11
    ELSE=12
    WHILE=13
    FOR=14
    IN=15
    TRY=16
    FINALLY=17
    WITH=18
    EXCEPT=19
    LAMBDA=20
    OR=21
    AND=22
    NOT=23
    IS=24
    NONE=25
    TRUE=26
    FALSE=27
    CLASS=28
    YIELD=29
    DEL=30
    PASS=31
    CONTINUE=32
    BREAK=33
    NEWLINE=34
    ID=35
    STRING=36
    INT=37
    FLOAT=38
    DOT=39
    ELLIPSE=40
    STAR=41
    OPEN_PAREN=42
    CLOSE_PAREN=43
    COMMA=44
    COLON=45
    SEMICOLON=46
    POWER=47
    ASSIGN=48
    OPEN_BRACK=49
    CLOSE_BRACK=50
    OR_OP=51
    XOR=52
    AND_OP=53
    LEFT_SHIFT=54
    RIGHT_SHIFT=55
    ADD=56
    MINUS=57
    DIV=58
    NOT_OP=59
    OPEN_BRACE=60
    CLOSE_BRACE=61
    LESS_THAN=62
    GREATER_THAN=63
    EQUALS=64
    GT_EQ=65
    LT_EQ=66
    NOT_EQ_1=67
    NOT_EQ_2=68
    AT=69
    ARROW=70
    SKIP_=71
    COMMENT=72
    INDENT=73
    DEDENT=74

    def __init__(self, input):
        super(SignalFlowV2Parser, self).__init__(input)
        self.checkVersion("4.5.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None



    class ProgramContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.ProgramContext, self).__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(SignalFlowV2Parser.EOF, 0)

        def NEWLINE(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.NEWLINE)
            else:
                return self.getToken(SignalFlowV2Parser.NEWLINE, i)

        def statement(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.StatementContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.StatementContext,i)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_program

        def enterRule(self, listener):
            if hasattr(listener, "enterProgram"):
                listener.enterProgram(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitProgram"):
                listener.exitProgram(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitProgram"):
                return visitor.visitProgram(self)
            else:
                return visitor.visitChildren(self)




    def program(self):

        localctx = SignalFlowV2Parser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 118
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << SignalFlowV2Parser.DEF) | (1 << SignalFlowV2Parser.RETURN) | (1 << SignalFlowV2Parser.FROM) | (1 << SignalFlowV2Parser.IMPORT) | (1 << SignalFlowV2Parser.ASSERT) | (1 << SignalFlowV2Parser.IF) | (1 << SignalFlowV2Parser.LAMBDA) | (1 << SignalFlowV2Parser.NOT) | (1 << SignalFlowV2Parser.NONE) | (1 << SignalFlowV2Parser.TRUE) | (1 << SignalFlowV2Parser.FALSE) | (1 << SignalFlowV2Parser.NEWLINE) | (1 << SignalFlowV2Parser.ID) | (1 << SignalFlowV2Parser.STRING) | (1 << SignalFlowV2Parser.INT) | (1 << SignalFlowV2Parser.FLOAT) | (1 << SignalFlowV2Parser.OPEN_PAREN) | (1 << SignalFlowV2Parser.OPEN_BRACK) | (1 << SignalFlowV2Parser.ADD) | (1 << SignalFlowV2Parser.MINUS) | (1 << SignalFlowV2Parser.NOT_OP) | (1 << SignalFlowV2Parser.OPEN_BRACE))) != 0) or _la==SignalFlowV2Parser.AT:
                self.state = 116
                token = self._input.LA(1)
                if token in [SignalFlowV2Parser.NEWLINE]:
                    self.state = 114
                    self.match(SignalFlowV2Parser.NEWLINE)

                elif token in [SignalFlowV2Parser.DEF, SignalFlowV2Parser.RETURN, SignalFlowV2Parser.FROM, SignalFlowV2Parser.IMPORT, SignalFlowV2Parser.ASSERT, SignalFlowV2Parser.IF, SignalFlowV2Parser.LAMBDA, SignalFlowV2Parser.NOT, SignalFlowV2Parser.NONE, SignalFlowV2Parser.TRUE, SignalFlowV2Parser.FALSE, SignalFlowV2Parser.ID, SignalFlowV2Parser.STRING, SignalFlowV2Parser.INT, SignalFlowV2Parser.FLOAT, SignalFlowV2Parser.OPEN_PAREN, SignalFlowV2Parser.OPEN_BRACK, SignalFlowV2Parser.ADD, SignalFlowV2Parser.MINUS, SignalFlowV2Parser.NOT_OP, SignalFlowV2Parser.OPEN_BRACE, SignalFlowV2Parser.AT]:
                    self.state = 115
                    self.statement()

                else:
                    raise NoViableAltException(self)

                self.state = 120
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 121
            self.match(SignalFlowV2Parser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Eval_inputContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Eval_inputContext, self).__init__(parent, invokingState)
            self.parser = parser

        def testlist(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.TestlistContext,0)


        def EOF(self):
            return self.getToken(SignalFlowV2Parser.EOF, 0)

        def NEWLINE(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.NEWLINE)
            else:
                return self.getToken(SignalFlowV2Parser.NEWLINE, i)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_eval_input

        def enterRule(self, listener):
            if hasattr(listener, "enterEval_input"):
                listener.enterEval_input(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitEval_input"):
                listener.exitEval_input(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitEval_input"):
                return visitor.visitEval_input(self)
            else:
                return visitor.visitChildren(self)




    def eval_input(self):

        localctx = SignalFlowV2Parser.Eval_inputContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_eval_input)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 123
            self.testlist()
            self.state = 127
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==SignalFlowV2Parser.NEWLINE:
                self.state = 124
                self.match(SignalFlowV2Parser.NEWLINE)
                self.state = 129
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 130
            self.match(SignalFlowV2Parser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class DecoratorContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.DecoratorContext, self).__init__(parent, invokingState)
            self.parser = parser

        def dotted_name(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Dotted_nameContext,0)


        def NEWLINE(self):
            return self.getToken(SignalFlowV2Parser.NEWLINE, 0)

        def actual_args(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Actual_argsContext,0)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_decorator

        def enterRule(self, listener):
            if hasattr(listener, "enterDecorator"):
                listener.enterDecorator(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitDecorator"):
                listener.exitDecorator(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitDecorator"):
                return visitor.visitDecorator(self)
            else:
                return visitor.visitChildren(self)




    def decorator(self):

        localctx = SignalFlowV2Parser.DecoratorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_decorator)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 132
            self.match(SignalFlowV2Parser.AT)
            self.state = 133
            self.dotted_name()
            self.state = 139
            _la = self._input.LA(1)
            if _la==SignalFlowV2Parser.OPEN_PAREN:
                self.state = 134
                self.match(SignalFlowV2Parser.OPEN_PAREN)
                self.state = 136
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << SignalFlowV2Parser.LAMBDA) | (1 << SignalFlowV2Parser.NOT) | (1 << SignalFlowV2Parser.NONE) | (1 << SignalFlowV2Parser.TRUE) | (1 << SignalFlowV2Parser.FALSE) | (1 << SignalFlowV2Parser.ID) | (1 << SignalFlowV2Parser.STRING) | (1 << SignalFlowV2Parser.INT) | (1 << SignalFlowV2Parser.FLOAT) | (1 << SignalFlowV2Parser.STAR) | (1 << SignalFlowV2Parser.OPEN_PAREN) | (1 << SignalFlowV2Parser.POWER) | (1 << SignalFlowV2Parser.OPEN_BRACK) | (1 << SignalFlowV2Parser.ADD) | (1 << SignalFlowV2Parser.MINUS) | (1 << SignalFlowV2Parser.NOT_OP) | (1 << SignalFlowV2Parser.OPEN_BRACE))) != 0):
                    self.state = 135
                    self.actual_args()


                self.state = 138
                self.match(SignalFlowV2Parser.CLOSE_PAREN)


            self.state = 141
            self.match(SignalFlowV2Parser.NEWLINE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class DecoratorsContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.DecoratorsContext, self).__init__(parent, invokingState)
            self.parser = parser

        def decorator(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.DecoratorContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.DecoratorContext,i)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_decorators

        def enterRule(self, listener):
            if hasattr(listener, "enterDecorators"):
                listener.enterDecorators(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitDecorators"):
                listener.exitDecorators(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitDecorators"):
                return visitor.visitDecorators(self)
            else:
                return visitor.visitChildren(self)




    def decorators(self):

        localctx = SignalFlowV2Parser.DecoratorsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_decorators)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 144 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 143
                self.decorator()
                self.state = 146 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==SignalFlowV2Parser.AT):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class DecoratedContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.DecoratedContext, self).__init__(parent, invokingState)
            self.parser = parser

        def decorators(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.DecoratorsContext,0)


        def function_definition(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Function_definitionContext,0)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_decorated

        def enterRule(self, listener):
            if hasattr(listener, "enterDecorated"):
                listener.enterDecorated(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitDecorated"):
                listener.exitDecorated(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitDecorated"):
                return visitor.visitDecorated(self)
            else:
                return visitor.visitChildren(self)




    def decorated(self):

        localctx = SignalFlowV2Parser.DecoratedContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_decorated)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 148
            self.decorators()
            self.state = 149
            self.function_definition()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Function_definitionContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Function_definitionContext, self).__init__(parent, invokingState)
            self.parser = parser

        def DEF(self):
            return self.getToken(SignalFlowV2Parser.DEF, 0)

        def ID(self):
            return self.getToken(SignalFlowV2Parser.ID, 0)

        def parameters(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.ParametersContext,0)


        def suite(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.SuiteContext,0)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_function_definition

        def enterRule(self, listener):
            if hasattr(listener, "enterFunction_definition"):
                listener.enterFunction_definition(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitFunction_definition"):
                listener.exitFunction_definition(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitFunction_definition"):
                return visitor.visitFunction_definition(self)
            else:
                return visitor.visitChildren(self)




    def function_definition(self):

        localctx = SignalFlowV2Parser.Function_definitionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_function_definition)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 151
            self.match(SignalFlowV2Parser.DEF)
            self.state = 152
            self.match(SignalFlowV2Parser.ID)
            self.state = 153
            self.parameters()
            self.state = 154
            self.match(SignalFlowV2Parser.COLON)
            self.state = 155
            self.suite()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ParametersContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.ParametersContext, self).__init__(parent, invokingState)
            self.parser = parser

        def OPEN_PAREN(self):
            return self.getToken(SignalFlowV2Parser.OPEN_PAREN, 0)

        def CLOSE_PAREN(self):
            return self.getToken(SignalFlowV2Parser.CLOSE_PAREN, 0)

        def var_args_list(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Var_args_listContext,0)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_parameters

        def enterRule(self, listener):
            if hasattr(listener, "enterParameters"):
                listener.enterParameters(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitParameters"):
                listener.exitParameters(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitParameters"):
                return visitor.visitParameters(self)
            else:
                return visitor.visitChildren(self)




    def parameters(self):

        localctx = SignalFlowV2Parser.ParametersContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_parameters)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 157
            self.match(SignalFlowV2Parser.OPEN_PAREN)
            self.state = 159
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << SignalFlowV2Parser.ID) | (1 << SignalFlowV2Parser.STAR) | (1 << SignalFlowV2Parser.POWER))) != 0):
                self.state = 158
                self.var_args_list()


            self.state = 161
            self.match(SignalFlowV2Parser.CLOSE_PAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Var_args_listContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Var_args_listContext, self).__init__(parent, invokingState)
            self.parser = parser

        def var_args_list_param_def(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.Var_args_list_param_defContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.Var_args_list_param_defContext,i)


        def var_args_star_param(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Var_args_star_paramContext,0)


        def var_args_kws_param(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Var_args_kws_paramContext,0)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_var_args_list

        def enterRule(self, listener):
            if hasattr(listener, "enterVar_args_list"):
                listener.enterVar_args_list(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitVar_args_list"):
                listener.exitVar_args_list(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitVar_args_list"):
                return visitor.visitVar_args_list(self)
            else:
                return visitor.visitChildren(self)




    def var_args_list(self):

        localctx = SignalFlowV2Parser.Var_args_listContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_var_args_list)
        self._la = 0 # Token type
        try:
            self.state = 188
            token = self._input.LA(1)
            if token in [SignalFlowV2Parser.ID]:
                self.enterOuterAlt(localctx, 1)
                self.state = 163
                self.var_args_list_param_def()
                self.state = 168
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,7,self._ctx)
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1:
                        self.state = 164
                        self.match(SignalFlowV2Parser.COMMA)
                        self.state = 165
                        self.var_args_list_param_def() 
                    self.state = 170
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,7,self._ctx)

                self.state = 180
                _la = self._input.LA(1)
                if _la==SignalFlowV2Parser.COMMA:
                    self.state = 171
                    self.match(SignalFlowV2Parser.COMMA)
                    self.state = 178
                    token = self._input.LA(1)
                    if token in [SignalFlowV2Parser.STAR]:
                        self.state = 172
                        self.var_args_star_param()
                        self.state = 175
                        _la = self._input.LA(1)
                        if _la==SignalFlowV2Parser.COMMA:
                            self.state = 173
                            self.match(SignalFlowV2Parser.COMMA)
                            self.state = 174
                            self.var_args_kws_param()


                        pass
                    elif token in [SignalFlowV2Parser.POWER]:
                        self.state = 177
                        self.var_args_kws_param()
                        pass
                    elif token in [SignalFlowV2Parser.CLOSE_PAREN]:
                        pass
                    else:
                        raise NoViableAltException(self)



            elif token in [SignalFlowV2Parser.STAR]:
                self.enterOuterAlt(localctx, 2)
                self.state = 182
                self.var_args_star_param()
                self.state = 185
                _la = self._input.LA(1)
                if _la==SignalFlowV2Parser.COMMA:
                    self.state = 183
                    self.match(SignalFlowV2Parser.COMMA)
                    self.state = 184
                    self.var_args_kws_param()



            elif token in [SignalFlowV2Parser.POWER]:
                self.enterOuterAlt(localctx, 3)
                self.state = 187
                self.var_args_kws_param()

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Var_args_star_paramContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Var_args_star_paramContext, self).__init__(parent, invokingState)
            self.parser = parser

        def STAR(self):
            return self.getToken(SignalFlowV2Parser.STAR, 0)

        def var_args_list_param_name(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Var_args_list_param_nameContext,0)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_var_args_star_param

        def enterRule(self, listener):
            if hasattr(listener, "enterVar_args_star_param"):
                listener.enterVar_args_star_param(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitVar_args_star_param"):
                listener.exitVar_args_star_param(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitVar_args_star_param"):
                return visitor.visitVar_args_star_param(self)
            else:
                return visitor.visitChildren(self)




    def var_args_star_param(self):

        localctx = SignalFlowV2Parser.Var_args_star_paramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_var_args_star_param)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 190
            self.match(SignalFlowV2Parser.STAR)
            self.state = 191
            self.var_args_list_param_name()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Var_args_kws_paramContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Var_args_kws_paramContext, self).__init__(parent, invokingState)
            self.parser = parser

        def POWER(self):
            return self.getToken(SignalFlowV2Parser.POWER, 0)

        def var_args_list_param_name(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Var_args_list_param_nameContext,0)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_var_args_kws_param

        def enterRule(self, listener):
            if hasattr(listener, "enterVar_args_kws_param"):
                listener.enterVar_args_kws_param(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitVar_args_kws_param"):
                listener.exitVar_args_kws_param(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitVar_args_kws_param"):
                return visitor.visitVar_args_kws_param(self)
            else:
                return visitor.visitChildren(self)




    def var_args_kws_param(self):

        localctx = SignalFlowV2Parser.Var_args_kws_paramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_var_args_kws_param)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 193
            self.match(SignalFlowV2Parser.POWER)
            self.state = 194
            self.var_args_list_param_name()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Var_args_list_param_defContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Var_args_list_param_defContext, self).__init__(parent, invokingState)
            self.parser = parser

        def var_args_list_param_name(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Var_args_list_param_nameContext,0)


        def test(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.TestContext,0)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_var_args_list_param_def

        def enterRule(self, listener):
            if hasattr(listener, "enterVar_args_list_param_def"):
                listener.enterVar_args_list_param_def(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitVar_args_list_param_def"):
                listener.exitVar_args_list_param_def(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitVar_args_list_param_def"):
                return visitor.visitVar_args_list_param_def(self)
            else:
                return visitor.visitChildren(self)




    def var_args_list_param_def(self):

        localctx = SignalFlowV2Parser.Var_args_list_param_defContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_var_args_list_param_def)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 196
            self.var_args_list_param_name()
            self.state = 199
            _la = self._input.LA(1)
            if _la==SignalFlowV2Parser.ASSIGN:
                self.state = 197
                self.match(SignalFlowV2Parser.ASSIGN)
                self.state = 198
                self.test()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Var_args_list_param_nameContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Var_args_list_param_nameContext, self).__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(SignalFlowV2Parser.ID, 0)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_var_args_list_param_name

        def enterRule(self, listener):
            if hasattr(listener, "enterVar_args_list_param_name"):
                listener.enterVar_args_list_param_name(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitVar_args_list_param_name"):
                listener.exitVar_args_list_param_name(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitVar_args_list_param_name"):
                return visitor.visitVar_args_list_param_name(self)
            else:
                return visitor.visitChildren(self)




    def var_args_list_param_name(self):

        localctx = SignalFlowV2Parser.Var_args_list_param_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_var_args_list_param_name)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 201
            self.match(SignalFlowV2Parser.ID)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class StatementContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.StatementContext, self).__init__(parent, invokingState)
            self.parser = parser

        def simple_statement(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Simple_statementContext,0)


        def compound_statement(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Compound_statementContext,0)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_statement

        def enterRule(self, listener):
            if hasattr(listener, "enterStatement"):
                listener.enterStatement(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitStatement"):
                listener.exitStatement(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitStatement"):
                return visitor.visitStatement(self)
            else:
                return visitor.visitChildren(self)




    def statement(self):

        localctx = SignalFlowV2Parser.StatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_statement)
        try:
            self.state = 205
            token = self._input.LA(1)
            if token in [SignalFlowV2Parser.RETURN, SignalFlowV2Parser.FROM, SignalFlowV2Parser.IMPORT, SignalFlowV2Parser.ASSERT, SignalFlowV2Parser.LAMBDA, SignalFlowV2Parser.NOT, SignalFlowV2Parser.NONE, SignalFlowV2Parser.TRUE, SignalFlowV2Parser.FALSE, SignalFlowV2Parser.ID, SignalFlowV2Parser.STRING, SignalFlowV2Parser.INT, SignalFlowV2Parser.FLOAT, SignalFlowV2Parser.OPEN_PAREN, SignalFlowV2Parser.OPEN_BRACK, SignalFlowV2Parser.ADD, SignalFlowV2Parser.MINUS, SignalFlowV2Parser.NOT_OP, SignalFlowV2Parser.OPEN_BRACE]:
                self.enterOuterAlt(localctx, 1)
                self.state = 203
                self.simple_statement()

            elif token in [SignalFlowV2Parser.DEF, SignalFlowV2Parser.IF, SignalFlowV2Parser.AT]:
                self.enterOuterAlt(localctx, 2)
                self.state = 204
                self.compound_statement()

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Simple_statementContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Simple_statementContext, self).__init__(parent, invokingState)
            self.parser = parser

        def small_statement(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.Small_statementContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.Small_statementContext,i)


        def NEWLINE(self):
            return self.getToken(SignalFlowV2Parser.NEWLINE, 0)

        def EOF(self):
            return self.getToken(SignalFlowV2Parser.EOF, 0)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_simple_statement

        def enterRule(self, listener):
            if hasattr(listener, "enterSimple_statement"):
                listener.enterSimple_statement(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitSimple_statement"):
                listener.exitSimple_statement(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitSimple_statement"):
                return visitor.visitSimple_statement(self)
            else:
                return visitor.visitChildren(self)




    def simple_statement(self):

        localctx = SignalFlowV2Parser.Simple_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_simple_statement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 207
            self.small_statement()
            self.state = 212
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,15,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 208
                    self.match(SignalFlowV2Parser.SEMICOLON)
                    self.state = 209
                    self.small_statement() 
                self.state = 214
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,15,self._ctx)

            self.state = 216
            _la = self._input.LA(1)
            if _la==SignalFlowV2Parser.SEMICOLON:
                self.state = 215
                self.match(SignalFlowV2Parser.SEMICOLON)


            self.state = 218
            _la = self._input.LA(1)
            if not(_la==SignalFlowV2Parser.EOF or _la==SignalFlowV2Parser.NEWLINE):
                self._errHandler.recoverInline(self)
            else:
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Small_statementContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Small_statementContext, self).__init__(parent, invokingState)
            self.parser = parser

        def expr_statement(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Expr_statementContext,0)


        def flow_statement(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Flow_statementContext,0)


        def import_statement(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Import_statementContext,0)


        def assert_statement(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Assert_statementContext,0)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_small_statement

        def enterRule(self, listener):
            if hasattr(listener, "enterSmall_statement"):
                listener.enterSmall_statement(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitSmall_statement"):
                listener.exitSmall_statement(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitSmall_statement"):
                return visitor.visitSmall_statement(self)
            else:
                return visitor.visitChildren(self)




    def small_statement(self):

        localctx = SignalFlowV2Parser.Small_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_small_statement)
        try:
            self.state = 224
            token = self._input.LA(1)
            if token in [SignalFlowV2Parser.LAMBDA, SignalFlowV2Parser.NOT, SignalFlowV2Parser.NONE, SignalFlowV2Parser.TRUE, SignalFlowV2Parser.FALSE, SignalFlowV2Parser.ID, SignalFlowV2Parser.STRING, SignalFlowV2Parser.INT, SignalFlowV2Parser.FLOAT, SignalFlowV2Parser.OPEN_PAREN, SignalFlowV2Parser.OPEN_BRACK, SignalFlowV2Parser.ADD, SignalFlowV2Parser.MINUS, SignalFlowV2Parser.NOT_OP, SignalFlowV2Parser.OPEN_BRACE]:
                self.enterOuterAlt(localctx, 1)
                self.state = 220
                self.expr_statement()

            elif token in [SignalFlowV2Parser.RETURN]:
                self.enterOuterAlt(localctx, 2)
                self.state = 221
                self.flow_statement()

            elif token in [SignalFlowV2Parser.FROM, SignalFlowV2Parser.IMPORT]:
                self.enterOuterAlt(localctx, 3)
                self.state = 222
                self.import_statement()

            elif token in [SignalFlowV2Parser.ASSERT]:
                self.enterOuterAlt(localctx, 4)
                self.state = 223
                self.assert_statement()

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Expr_statementContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Expr_statementContext, self).__init__(parent, invokingState)
            self.parser = parser

        def testlist(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.TestlistContext,0)


        def id_list(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Id_listContext,0)


        def ASSIGN(self):
            return self.getToken(SignalFlowV2Parser.ASSIGN, 0)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_expr_statement

        def enterRule(self, listener):
            if hasattr(listener, "enterExpr_statement"):
                listener.enterExpr_statement(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitExpr_statement"):
                listener.exitExpr_statement(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitExpr_statement"):
                return visitor.visitExpr_statement(self)
            else:
                return visitor.visitChildren(self)




    def expr_statement(self):

        localctx = SignalFlowV2Parser.Expr_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_expr_statement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 229
            self._errHandler.sync(self);
            la_ = self._interp.adaptivePredict(self._input,18,self._ctx)
            if la_ == 1:
                self.state = 226
                self.id_list()
                self.state = 227
                self.match(SignalFlowV2Parser.ASSIGN)


            self.state = 231
            self.testlist()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Id_listContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Id_listContext, self).__init__(parent, invokingState)
            self.parser = parser

        def ID(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.ID)
            else:
                return self.getToken(SignalFlowV2Parser.ID, i)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_id_list

        def enterRule(self, listener):
            if hasattr(listener, "enterId_list"):
                listener.enterId_list(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitId_list"):
                listener.exitId_list(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitId_list"):
                return visitor.visitId_list(self)
            else:
                return visitor.visitChildren(self)




    def id_list(self):

        localctx = SignalFlowV2Parser.Id_listContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_id_list)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 233
            self.match(SignalFlowV2Parser.ID)
            self.state = 238
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,19,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 234
                    self.match(SignalFlowV2Parser.COMMA)
                    self.state = 235
                    self.match(SignalFlowV2Parser.ID) 
                self.state = 240
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,19,self._ctx)

            self.state = 242
            _la = self._input.LA(1)
            if _la==SignalFlowV2Parser.COMMA:
                self.state = 241
                self.match(SignalFlowV2Parser.COMMA)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Import_statementContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Import_statementContext, self).__init__(parent, invokingState)
            self.parser = parser

        def import_name(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Import_nameContext,0)


        def import_from(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Import_fromContext,0)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_import_statement

        def enterRule(self, listener):
            if hasattr(listener, "enterImport_statement"):
                listener.enterImport_statement(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitImport_statement"):
                listener.exitImport_statement(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitImport_statement"):
                return visitor.visitImport_statement(self)
            else:
                return visitor.visitChildren(self)




    def import_statement(self):

        localctx = SignalFlowV2Parser.Import_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_import_statement)
        try:
            self.state = 246
            token = self._input.LA(1)
            if token in [SignalFlowV2Parser.IMPORT]:
                self.enterOuterAlt(localctx, 1)
                self.state = 244
                self.import_name()

            elif token in [SignalFlowV2Parser.FROM]:
                self.enterOuterAlt(localctx, 2)
                self.state = 245
                self.import_from()

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Import_nameContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Import_nameContext, self).__init__(parent, invokingState)
            self.parser = parser

        def IMPORT(self):
            return self.getToken(SignalFlowV2Parser.IMPORT, 0)

        def dotted_as_names(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Dotted_as_namesContext,0)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_import_name

        def enterRule(self, listener):
            if hasattr(listener, "enterImport_name"):
                listener.enterImport_name(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitImport_name"):
                listener.exitImport_name(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitImport_name"):
                return visitor.visitImport_name(self)
            else:
                return visitor.visitChildren(self)




    def import_name(self):

        localctx = SignalFlowV2Parser.Import_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_import_name)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 248
            self.match(SignalFlowV2Parser.IMPORT)
            self.state = 249
            self.dotted_as_names()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Import_fromContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Import_fromContext, self).__init__(parent, invokingState)
            self.parser = parser

        def FROM(self):
            return self.getToken(SignalFlowV2Parser.FROM, 0)

        def dotted_name(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Dotted_nameContext,0)


        def IMPORT(self):
            return self.getToken(SignalFlowV2Parser.IMPORT, 0)

        def import_as_names(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Import_as_namesContext,0)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_import_from

        def enterRule(self, listener):
            if hasattr(listener, "enterImport_from"):
                listener.enterImport_from(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitImport_from"):
                listener.exitImport_from(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitImport_from"):
                return visitor.visitImport_from(self)
            else:
                return visitor.visitChildren(self)




    def import_from(self):

        localctx = SignalFlowV2Parser.Import_fromContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_import_from)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 251
            self.match(SignalFlowV2Parser.FROM)
            self.state = 252
            self.dotted_name()
            self.state = 253
            self.match(SignalFlowV2Parser.IMPORT)
            self.state = 260
            token = self._input.LA(1)
            if token in [SignalFlowV2Parser.STAR]:
                self.state = 254
                self.match(SignalFlowV2Parser.STAR)

            elif token in [SignalFlowV2Parser.OPEN_PAREN]:
                self.state = 255
                self.match(SignalFlowV2Parser.OPEN_PAREN)
                self.state = 256
                self.import_as_names()
                self.state = 257
                self.match(SignalFlowV2Parser.CLOSE_PAREN)

            elif token in [SignalFlowV2Parser.ID]:
                self.state = 259
                self.import_as_names()

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Import_as_nameContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Import_as_nameContext, self).__init__(parent, invokingState)
            self.parser = parser

        def ID(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.ID)
            else:
                return self.getToken(SignalFlowV2Parser.ID, i)

        def AS(self):
            return self.getToken(SignalFlowV2Parser.AS, 0)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_import_as_name

        def enterRule(self, listener):
            if hasattr(listener, "enterImport_as_name"):
                listener.enterImport_as_name(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitImport_as_name"):
                listener.exitImport_as_name(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitImport_as_name"):
                return visitor.visitImport_as_name(self)
            else:
                return visitor.visitChildren(self)




    def import_as_name(self):

        localctx = SignalFlowV2Parser.Import_as_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_import_as_name)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 262
            self.match(SignalFlowV2Parser.ID)
            self.state = 265
            _la = self._input.LA(1)
            if _la==SignalFlowV2Parser.AS:
                self.state = 263
                self.match(SignalFlowV2Parser.AS)
                self.state = 264
                self.match(SignalFlowV2Parser.ID)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Dotted_as_nameContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Dotted_as_nameContext, self).__init__(parent, invokingState)
            self.parser = parser

        def dotted_name(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Dotted_nameContext,0)


        def AS(self):
            return self.getToken(SignalFlowV2Parser.AS, 0)

        def ID(self):
            return self.getToken(SignalFlowV2Parser.ID, 0)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_dotted_as_name

        def enterRule(self, listener):
            if hasattr(listener, "enterDotted_as_name"):
                listener.enterDotted_as_name(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitDotted_as_name"):
                listener.exitDotted_as_name(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitDotted_as_name"):
                return visitor.visitDotted_as_name(self)
            else:
                return visitor.visitChildren(self)




    def dotted_as_name(self):

        localctx = SignalFlowV2Parser.Dotted_as_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_dotted_as_name)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 267
            self.dotted_name()
            self.state = 270
            _la = self._input.LA(1)
            if _la==SignalFlowV2Parser.AS:
                self.state = 268
                self.match(SignalFlowV2Parser.AS)
                self.state = 269
                self.match(SignalFlowV2Parser.ID)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Import_as_namesContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Import_as_namesContext, self).__init__(parent, invokingState)
            self.parser = parser

        def import_as_name(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.Import_as_nameContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.Import_as_nameContext,i)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_import_as_names

        def enterRule(self, listener):
            if hasattr(listener, "enterImport_as_names"):
                listener.enterImport_as_names(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitImport_as_names"):
                listener.exitImport_as_names(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitImport_as_names"):
                return visitor.visitImport_as_names(self)
            else:
                return visitor.visitChildren(self)




    def import_as_names(self):

        localctx = SignalFlowV2Parser.Import_as_namesContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_import_as_names)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 272
            self.import_as_name()
            self.state = 277
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,25,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 273
                    self.match(SignalFlowV2Parser.COMMA)
                    self.state = 274
                    self.import_as_name() 
                self.state = 279
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,25,self._ctx)

            self.state = 281
            _la = self._input.LA(1)
            if _la==SignalFlowV2Parser.COMMA:
                self.state = 280
                self.match(SignalFlowV2Parser.COMMA)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Dotted_as_namesContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Dotted_as_namesContext, self).__init__(parent, invokingState)
            self.parser = parser

        def dotted_as_name(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.Dotted_as_nameContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.Dotted_as_nameContext,i)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_dotted_as_names

        def enterRule(self, listener):
            if hasattr(listener, "enterDotted_as_names"):
                listener.enterDotted_as_names(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitDotted_as_names"):
                listener.exitDotted_as_names(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitDotted_as_names"):
                return visitor.visitDotted_as_names(self)
            else:
                return visitor.visitChildren(self)




    def dotted_as_names(self):

        localctx = SignalFlowV2Parser.Dotted_as_namesContext(self, self._ctx, self.state)
        self.enterRule(localctx, 46, self.RULE_dotted_as_names)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 283
            self.dotted_as_name()
            self.state = 288
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==SignalFlowV2Parser.COMMA:
                self.state = 284
                self.match(SignalFlowV2Parser.COMMA)
                self.state = 285
                self.dotted_as_name()
                self.state = 290
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Dotted_nameContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Dotted_nameContext, self).__init__(parent, invokingState)
            self.parser = parser

        def ID(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.ID)
            else:
                return self.getToken(SignalFlowV2Parser.ID, i)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_dotted_name

        def enterRule(self, listener):
            if hasattr(listener, "enterDotted_name"):
                listener.enterDotted_name(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitDotted_name"):
                listener.exitDotted_name(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitDotted_name"):
                return visitor.visitDotted_name(self)
            else:
                return visitor.visitChildren(self)




    def dotted_name(self):

        localctx = SignalFlowV2Parser.Dotted_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 48, self.RULE_dotted_name)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 291
            self.match(SignalFlowV2Parser.ID)
            self.state = 296
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==SignalFlowV2Parser.DOT:
                self.state = 292
                self.match(SignalFlowV2Parser.DOT)
                self.state = 293
                self.match(SignalFlowV2Parser.ID)
                self.state = 298
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Return_statementContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Return_statementContext, self).__init__(parent, invokingState)
            self.parser = parser

        def RETURN(self):
            return self.getToken(SignalFlowV2Parser.RETURN, 0)

        def testlist(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.TestlistContext,0)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_return_statement

        def enterRule(self, listener):
            if hasattr(listener, "enterReturn_statement"):
                listener.enterReturn_statement(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitReturn_statement"):
                listener.exitReturn_statement(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitReturn_statement"):
                return visitor.visitReturn_statement(self)
            else:
                return visitor.visitChildren(self)




    def return_statement(self):

        localctx = SignalFlowV2Parser.Return_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 50, self.RULE_return_statement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 299
            self.match(SignalFlowV2Parser.RETURN)
            self.state = 301
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << SignalFlowV2Parser.LAMBDA) | (1 << SignalFlowV2Parser.NOT) | (1 << SignalFlowV2Parser.NONE) | (1 << SignalFlowV2Parser.TRUE) | (1 << SignalFlowV2Parser.FALSE) | (1 << SignalFlowV2Parser.ID) | (1 << SignalFlowV2Parser.STRING) | (1 << SignalFlowV2Parser.INT) | (1 << SignalFlowV2Parser.FLOAT) | (1 << SignalFlowV2Parser.OPEN_PAREN) | (1 << SignalFlowV2Parser.OPEN_BRACK) | (1 << SignalFlowV2Parser.ADD) | (1 << SignalFlowV2Parser.MINUS) | (1 << SignalFlowV2Parser.NOT_OP) | (1 << SignalFlowV2Parser.OPEN_BRACE))) != 0):
                self.state = 300
                self.testlist()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Flow_statementContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Flow_statementContext, self).__init__(parent, invokingState)
            self.parser = parser

        def return_statement(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Return_statementContext,0)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_flow_statement

        def enterRule(self, listener):
            if hasattr(listener, "enterFlow_statement"):
                listener.enterFlow_statement(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitFlow_statement"):
                listener.exitFlow_statement(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitFlow_statement"):
                return visitor.visitFlow_statement(self)
            else:
                return visitor.visitChildren(self)




    def flow_statement(self):

        localctx = SignalFlowV2Parser.Flow_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 52, self.RULE_flow_statement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 303
            self.return_statement()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Compound_statementContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Compound_statementContext, self).__init__(parent, invokingState)
            self.parser = parser

        def if_statement(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.If_statementContext,0)


        def function_definition(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Function_definitionContext,0)


        def decorated(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.DecoratedContext,0)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_compound_statement

        def enterRule(self, listener):
            if hasattr(listener, "enterCompound_statement"):
                listener.enterCompound_statement(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitCompound_statement"):
                listener.exitCompound_statement(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitCompound_statement"):
                return visitor.visitCompound_statement(self)
            else:
                return visitor.visitChildren(self)




    def compound_statement(self):

        localctx = SignalFlowV2Parser.Compound_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 54, self.RULE_compound_statement)
        try:
            self.state = 308
            token = self._input.LA(1)
            if token in [SignalFlowV2Parser.IF]:
                self.enterOuterAlt(localctx, 1)
                self.state = 305
                self.if_statement()

            elif token in [SignalFlowV2Parser.DEF]:
                self.enterOuterAlt(localctx, 2)
                self.state = 306
                self.function_definition()

            elif token in [SignalFlowV2Parser.AT]:
                self.enterOuterAlt(localctx, 3)
                self.state = 307
                self.decorated()

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Assert_statementContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Assert_statementContext, self).__init__(parent, invokingState)
            self.parser = parser

        def ASSERT(self):
            return self.getToken(SignalFlowV2Parser.ASSERT, 0)

        def test(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.TestContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.TestContext,i)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_assert_statement

        def enterRule(self, listener):
            if hasattr(listener, "enterAssert_statement"):
                listener.enterAssert_statement(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitAssert_statement"):
                listener.exitAssert_statement(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitAssert_statement"):
                return visitor.visitAssert_statement(self)
            else:
                return visitor.visitChildren(self)




    def assert_statement(self):

        localctx = SignalFlowV2Parser.Assert_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 56, self.RULE_assert_statement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 310
            self.match(SignalFlowV2Parser.ASSERT)
            self.state = 311
            self.test()
            self.state = 314
            _la = self._input.LA(1)
            if _la==SignalFlowV2Parser.COMMA:
                self.state = 312
                self.match(SignalFlowV2Parser.COMMA)
                self.state = 313
                self.test()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class If_statementContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.If_statementContext, self).__init__(parent, invokingState)
            self.parser = parser

        def IF(self):
            return self.getToken(SignalFlowV2Parser.IF, 0)

        def test(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.TestContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.TestContext,i)


        def suite(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.SuiteContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.SuiteContext,i)


        def ELIF(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.ELIF)
            else:
                return self.getToken(SignalFlowV2Parser.ELIF, i)

        def ELSE(self):
            return self.getToken(SignalFlowV2Parser.ELSE, 0)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_if_statement

        def enterRule(self, listener):
            if hasattr(listener, "enterIf_statement"):
                listener.enterIf_statement(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitIf_statement"):
                listener.exitIf_statement(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitIf_statement"):
                return visitor.visitIf_statement(self)
            else:
                return visitor.visitChildren(self)




    def if_statement(self):

        localctx = SignalFlowV2Parser.If_statementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 58, self.RULE_if_statement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 316
            self.match(SignalFlowV2Parser.IF)
            self.state = 317
            self.test()
            self.state = 318
            self.match(SignalFlowV2Parser.COLON)
            self.state = 319
            self.suite()
            self.state = 327
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==SignalFlowV2Parser.ELIF:
                self.state = 320
                self.match(SignalFlowV2Parser.ELIF)
                self.state = 321
                self.test()
                self.state = 322
                self.match(SignalFlowV2Parser.COLON)
                self.state = 323
                self.suite()
                self.state = 329
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 333
            _la = self._input.LA(1)
            if _la==SignalFlowV2Parser.ELSE:
                self.state = 330
                self.match(SignalFlowV2Parser.ELSE)
                self.state = 331
                self.match(SignalFlowV2Parser.COLON)
                self.state = 332
                self.suite()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class SuiteContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.SuiteContext, self).__init__(parent, invokingState)
            self.parser = parser

        def simple_statement(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Simple_statementContext,0)


        def NEWLINE(self):
            return self.getToken(SignalFlowV2Parser.NEWLINE, 0)

        def INDENT(self):
            return self.getToken(SignalFlowV2Parser.INDENT, 0)

        def DEDENT(self):
            return self.getToken(SignalFlowV2Parser.DEDENT, 0)

        def statement(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.StatementContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.StatementContext,i)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_suite

        def enterRule(self, listener):
            if hasattr(listener, "enterSuite"):
                listener.enterSuite(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitSuite"):
                listener.exitSuite(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitSuite"):
                return visitor.visitSuite(self)
            else:
                return visitor.visitChildren(self)




    def suite(self):

        localctx = SignalFlowV2Parser.SuiteContext(self, self._ctx, self.state)
        self.enterRule(localctx, 60, self.RULE_suite)
        self._la = 0 # Token type
        try:
            self.state = 345
            token = self._input.LA(1)
            if token in [SignalFlowV2Parser.RETURN, SignalFlowV2Parser.FROM, SignalFlowV2Parser.IMPORT, SignalFlowV2Parser.ASSERT, SignalFlowV2Parser.LAMBDA, SignalFlowV2Parser.NOT, SignalFlowV2Parser.NONE, SignalFlowV2Parser.TRUE, SignalFlowV2Parser.FALSE, SignalFlowV2Parser.ID, SignalFlowV2Parser.STRING, SignalFlowV2Parser.INT, SignalFlowV2Parser.FLOAT, SignalFlowV2Parser.OPEN_PAREN, SignalFlowV2Parser.OPEN_BRACK, SignalFlowV2Parser.ADD, SignalFlowV2Parser.MINUS, SignalFlowV2Parser.NOT_OP, SignalFlowV2Parser.OPEN_BRACE]:
                self.enterOuterAlt(localctx, 1)
                self.state = 335
                self.simple_statement()

            elif token in [SignalFlowV2Parser.NEWLINE]:
                self.enterOuterAlt(localctx, 2)
                self.state = 336
                self.match(SignalFlowV2Parser.NEWLINE)
                self.state = 337
                self.match(SignalFlowV2Parser.INDENT)
                self.state = 339 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 338
                    self.statement()
                    self.state = 341 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << SignalFlowV2Parser.DEF) | (1 << SignalFlowV2Parser.RETURN) | (1 << SignalFlowV2Parser.FROM) | (1 << SignalFlowV2Parser.IMPORT) | (1 << SignalFlowV2Parser.ASSERT) | (1 << SignalFlowV2Parser.IF) | (1 << SignalFlowV2Parser.LAMBDA) | (1 << SignalFlowV2Parser.NOT) | (1 << SignalFlowV2Parser.NONE) | (1 << SignalFlowV2Parser.TRUE) | (1 << SignalFlowV2Parser.FALSE) | (1 << SignalFlowV2Parser.ID) | (1 << SignalFlowV2Parser.STRING) | (1 << SignalFlowV2Parser.INT) | (1 << SignalFlowV2Parser.FLOAT) | (1 << SignalFlowV2Parser.OPEN_PAREN) | (1 << SignalFlowV2Parser.OPEN_BRACK) | (1 << SignalFlowV2Parser.ADD) | (1 << SignalFlowV2Parser.MINUS) | (1 << SignalFlowV2Parser.NOT_OP) | (1 << SignalFlowV2Parser.OPEN_BRACE))) != 0) or _la==SignalFlowV2Parser.AT):
                        break

                self.state = 343
                self.match(SignalFlowV2Parser.DEDENT)

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class TestContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.TestContext, self).__init__(parent, invokingState)
            self.parser = parser

        def or_test(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.Or_testContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.Or_testContext,i)


        def IF(self):
            return self.getToken(SignalFlowV2Parser.IF, 0)

        def ELSE(self):
            return self.getToken(SignalFlowV2Parser.ELSE, 0)

        def test(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.TestContext,0)


        def lambdef(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.LambdefContext,0)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_test

        def enterRule(self, listener):
            if hasattr(listener, "enterTest"):
                listener.enterTest(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitTest"):
                listener.exitTest(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitTest"):
                return visitor.visitTest(self)
            else:
                return visitor.visitChildren(self)




    def test(self):

        localctx = SignalFlowV2Parser.TestContext(self, self._ctx, self.state)
        self.enterRule(localctx, 62, self.RULE_test)
        self._la = 0 # Token type
        try:
            self.state = 356
            token = self._input.LA(1)
            if token in [SignalFlowV2Parser.NOT, SignalFlowV2Parser.NONE, SignalFlowV2Parser.TRUE, SignalFlowV2Parser.FALSE, SignalFlowV2Parser.ID, SignalFlowV2Parser.STRING, SignalFlowV2Parser.INT, SignalFlowV2Parser.FLOAT, SignalFlowV2Parser.OPEN_PAREN, SignalFlowV2Parser.OPEN_BRACK, SignalFlowV2Parser.ADD, SignalFlowV2Parser.MINUS, SignalFlowV2Parser.NOT_OP, SignalFlowV2Parser.OPEN_BRACE]:
                self.enterOuterAlt(localctx, 1)
                self.state = 347
                self.or_test()
                self.state = 353
                _la = self._input.LA(1)
                if _la==SignalFlowV2Parser.IF:
                    self.state = 348
                    self.match(SignalFlowV2Parser.IF)
                    self.state = 349
                    self.or_test()
                    self.state = 350
                    self.match(SignalFlowV2Parser.ELSE)
                    self.state = 351
                    self.test()



            elif token in [SignalFlowV2Parser.LAMBDA]:
                self.enterOuterAlt(localctx, 2)
                self.state = 355
                self.lambdef()

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class LambdefContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.LambdefContext, self).__init__(parent, invokingState)
            self.parser = parser

        def LAMBDA(self):
            return self.getToken(SignalFlowV2Parser.LAMBDA, 0)

        def ID(self):
            return self.getToken(SignalFlowV2Parser.ID, 0)

        def COLON(self):
            return self.getToken(SignalFlowV2Parser.COLON, 0)

        def test(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.TestContext,0)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_lambdef

        def enterRule(self, listener):
            if hasattr(listener, "enterLambdef"):
                listener.enterLambdef(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitLambdef"):
                listener.exitLambdef(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitLambdef"):
                return visitor.visitLambdef(self)
            else:
                return visitor.visitChildren(self)




    def lambdef(self):

        localctx = SignalFlowV2Parser.LambdefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 64, self.RULE_lambdef)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 358
            self.match(SignalFlowV2Parser.LAMBDA)
            self.state = 359
            self.match(SignalFlowV2Parser.ID)
            self.state = 360
            self.match(SignalFlowV2Parser.COLON)
            self.state = 361
            self.test()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Or_testContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Or_testContext, self).__init__(parent, invokingState)
            self.parser = parser

        def and_test(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.And_testContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.And_testContext,i)


        def OR(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.OR)
            else:
                return self.getToken(SignalFlowV2Parser.OR, i)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_or_test

        def enterRule(self, listener):
            if hasattr(listener, "enterOr_test"):
                listener.enterOr_test(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitOr_test"):
                listener.exitOr_test(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitOr_test"):
                return visitor.visitOr_test(self)
            else:
                return visitor.visitChildren(self)




    def or_test(self):

        localctx = SignalFlowV2Parser.Or_testContext(self, self._ctx, self.state)
        self.enterRule(localctx, 66, self.RULE_or_test)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 363
            self.and_test()
            self.state = 368
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==SignalFlowV2Parser.OR:
                self.state = 364
                self.match(SignalFlowV2Parser.OR)
                self.state = 365
                self.and_test()
                self.state = 370
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class And_testContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.And_testContext, self).__init__(parent, invokingState)
            self.parser = parser

        def not_test(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.Not_testContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.Not_testContext,i)


        def AND(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.AND)
            else:
                return self.getToken(SignalFlowV2Parser.AND, i)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_and_test

        def enterRule(self, listener):
            if hasattr(listener, "enterAnd_test"):
                listener.enterAnd_test(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitAnd_test"):
                listener.exitAnd_test(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitAnd_test"):
                return visitor.visitAnd_test(self)
            else:
                return visitor.visitChildren(self)




    def and_test(self):

        localctx = SignalFlowV2Parser.And_testContext(self, self._ctx, self.state)
        self.enterRule(localctx, 68, self.RULE_and_test)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 371
            self.not_test()
            self.state = 376
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==SignalFlowV2Parser.AND:
                self.state = 372
                self.match(SignalFlowV2Parser.AND)
                self.state = 373
                self.not_test()
                self.state = 378
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Not_testContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Not_testContext, self).__init__(parent, invokingState)
            self.parser = parser

        def NOT(self):
            return self.getToken(SignalFlowV2Parser.NOT, 0)

        def not_test(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Not_testContext,0)


        def comparison(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.ComparisonContext,0)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_not_test

        def enterRule(self, listener):
            if hasattr(listener, "enterNot_test"):
                listener.enterNot_test(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitNot_test"):
                listener.exitNot_test(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitNot_test"):
                return visitor.visitNot_test(self)
            else:
                return visitor.visitChildren(self)




    def not_test(self):

        localctx = SignalFlowV2Parser.Not_testContext(self, self._ctx, self.state)
        self.enterRule(localctx, 70, self.RULE_not_test)
        try:
            self.state = 382
            token = self._input.LA(1)
            if token in [SignalFlowV2Parser.NOT]:
                self.enterOuterAlt(localctx, 1)
                self.state = 379
                self.match(SignalFlowV2Parser.NOT)
                self.state = 380
                self.not_test()

            elif token in [SignalFlowV2Parser.NONE, SignalFlowV2Parser.TRUE, SignalFlowV2Parser.FALSE, SignalFlowV2Parser.ID, SignalFlowV2Parser.STRING, SignalFlowV2Parser.INT, SignalFlowV2Parser.FLOAT, SignalFlowV2Parser.OPEN_PAREN, SignalFlowV2Parser.OPEN_BRACK, SignalFlowV2Parser.ADD, SignalFlowV2Parser.MINUS, SignalFlowV2Parser.NOT_OP, SignalFlowV2Parser.OPEN_BRACE]:
                self.enterOuterAlt(localctx, 2)
                self.state = 381
                self.comparison()

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ComparisonContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.ComparisonContext, self).__init__(parent, invokingState)
            self.parser = parser

        def expr(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.ExprContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.ExprContext,i)


        def LESS_THAN(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.LESS_THAN)
            else:
                return self.getToken(SignalFlowV2Parser.LESS_THAN, i)

        def LT_EQ(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.LT_EQ)
            else:
                return self.getToken(SignalFlowV2Parser.LT_EQ, i)

        def EQUALS(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.EQUALS)
            else:
                return self.getToken(SignalFlowV2Parser.EQUALS, i)

        def NOT_EQ_1(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.NOT_EQ_1)
            else:
                return self.getToken(SignalFlowV2Parser.NOT_EQ_1, i)

        def NOT_EQ_2(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.NOT_EQ_2)
            else:
                return self.getToken(SignalFlowV2Parser.NOT_EQ_2, i)

        def GREATER_THAN(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.GREATER_THAN)
            else:
                return self.getToken(SignalFlowV2Parser.GREATER_THAN, i)

        def GT_EQ(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.GT_EQ)
            else:
                return self.getToken(SignalFlowV2Parser.GT_EQ, i)

        def IS(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.IS)
            else:
                return self.getToken(SignalFlowV2Parser.IS, i)

        def NOT(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.NOT)
            else:
                return self.getToken(SignalFlowV2Parser.NOT, i)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_comparison

        def enterRule(self, listener):
            if hasattr(listener, "enterComparison"):
                listener.enterComparison(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitComparison"):
                listener.exitComparison(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitComparison"):
                return visitor.visitComparison(self)
            else:
                return visitor.visitChildren(self)




    def comparison(self):

        localctx = SignalFlowV2Parser.ComparisonContext(self, self._ctx, self.state)
        self.enterRule(localctx, 72, self.RULE_comparison)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 384
            self.expr()
            self.state = 400
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while ((((_la - 24)) & ~0x3f) == 0 and ((1 << (_la - 24)) & ((1 << (SignalFlowV2Parser.IS - 24)) | (1 << (SignalFlowV2Parser.LESS_THAN - 24)) | (1 << (SignalFlowV2Parser.GREATER_THAN - 24)) | (1 << (SignalFlowV2Parser.EQUALS - 24)) | (1 << (SignalFlowV2Parser.GT_EQ - 24)) | (1 << (SignalFlowV2Parser.LT_EQ - 24)) | (1 << (SignalFlowV2Parser.NOT_EQ_1 - 24)) | (1 << (SignalFlowV2Parser.NOT_EQ_2 - 24)))) != 0):
                self.state = 395
                self._errHandler.sync(self);
                la_ = self._interp.adaptivePredict(self._input,41,self._ctx)
                if la_ == 1:
                    self.state = 385
                    self.match(SignalFlowV2Parser.LESS_THAN)
                    pass

                elif la_ == 2:
                    self.state = 386
                    self.match(SignalFlowV2Parser.LT_EQ)
                    pass

                elif la_ == 3:
                    self.state = 387
                    self.match(SignalFlowV2Parser.EQUALS)
                    pass

                elif la_ == 4:
                    self.state = 388
                    self.match(SignalFlowV2Parser.NOT_EQ_1)
                    pass

                elif la_ == 5:
                    self.state = 389
                    self.match(SignalFlowV2Parser.NOT_EQ_2)
                    pass

                elif la_ == 6:
                    self.state = 390
                    self.match(SignalFlowV2Parser.GREATER_THAN)
                    pass

                elif la_ == 7:
                    self.state = 391
                    self.match(SignalFlowV2Parser.GT_EQ)
                    pass

                elif la_ == 8:
                    self.state = 392
                    self.match(SignalFlowV2Parser.IS)
                    pass

                elif la_ == 9:
                    self.state = 393
                    self.match(SignalFlowV2Parser.IS)
                    self.state = 394
                    self.match(SignalFlowV2Parser.NOT)
                    pass


                self.state = 397
                self.expr()
                self.state = 402
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ExprContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.ExprContext, self).__init__(parent, invokingState)
            self.parser = parser

        def xor_expr(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.Xor_exprContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.Xor_exprContext,i)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_expr

        def enterRule(self, listener):
            if hasattr(listener, "enterExpr"):
                listener.enterExpr(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitExpr"):
                listener.exitExpr(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitExpr"):
                return visitor.visitExpr(self)
            else:
                return visitor.visitChildren(self)




    def expr(self):

        localctx = SignalFlowV2Parser.ExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 74, self.RULE_expr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 403
            self.xor_expr()
            self.state = 408
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==SignalFlowV2Parser.OR_OP:
                self.state = 404
                self.match(SignalFlowV2Parser.OR_OP)
                self.state = 405
                self.xor_expr()
                self.state = 410
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Xor_exprContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Xor_exprContext, self).__init__(parent, invokingState)
            self.parser = parser

        def and_expr(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.And_exprContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.And_exprContext,i)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_xor_expr

        def enterRule(self, listener):
            if hasattr(listener, "enterXor_expr"):
                listener.enterXor_expr(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitXor_expr"):
                listener.exitXor_expr(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitXor_expr"):
                return visitor.visitXor_expr(self)
            else:
                return visitor.visitChildren(self)




    def xor_expr(self):

        localctx = SignalFlowV2Parser.Xor_exprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 76, self.RULE_xor_expr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 411
            self.and_expr()
            self.state = 416
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==SignalFlowV2Parser.XOR:
                self.state = 412
                self.match(SignalFlowV2Parser.XOR)
                self.state = 413
                self.and_expr()
                self.state = 418
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class And_exprContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.And_exprContext, self).__init__(parent, invokingState)
            self.parser = parser

        def shift_expr(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.Shift_exprContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.Shift_exprContext,i)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_and_expr

        def enterRule(self, listener):
            if hasattr(listener, "enterAnd_expr"):
                listener.enterAnd_expr(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitAnd_expr"):
                listener.exitAnd_expr(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitAnd_expr"):
                return visitor.visitAnd_expr(self)
            else:
                return visitor.visitChildren(self)




    def and_expr(self):

        localctx = SignalFlowV2Parser.And_exprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 78, self.RULE_and_expr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 419
            self.shift_expr()
            self.state = 424
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==SignalFlowV2Parser.AND_OP:
                self.state = 420
                self.match(SignalFlowV2Parser.AND_OP)
                self.state = 421
                self.shift_expr()
                self.state = 426
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Shift_exprContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Shift_exprContext, self).__init__(parent, invokingState)
            self.parser = parser

        def arith_expr(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.Arith_exprContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.Arith_exprContext,i)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_shift_expr

        def enterRule(self, listener):
            if hasattr(listener, "enterShift_expr"):
                listener.enterShift_expr(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitShift_expr"):
                listener.exitShift_expr(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitShift_expr"):
                return visitor.visitShift_expr(self)
            else:
                return visitor.visitChildren(self)




    def shift_expr(self):

        localctx = SignalFlowV2Parser.Shift_exprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 80, self.RULE_shift_expr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 427
            self.arith_expr()
            self.state = 434
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==SignalFlowV2Parser.LEFT_SHIFT or _la==SignalFlowV2Parser.RIGHT_SHIFT:
                self.state = 432
                token = self._input.LA(1)
                if token in [SignalFlowV2Parser.LEFT_SHIFT]:
                    self.state = 428
                    self.match(SignalFlowV2Parser.LEFT_SHIFT)
                    self.state = 429
                    self.arith_expr()

                elif token in [SignalFlowV2Parser.RIGHT_SHIFT]:
                    self.state = 430
                    self.match(SignalFlowV2Parser.RIGHT_SHIFT)
                    self.state = 431
                    self.arith_expr()

                else:
                    raise NoViableAltException(self)

                self.state = 436
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Arith_exprContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Arith_exprContext, self).__init__(parent, invokingState)
            self.parser = parser

        def term(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.TermContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.TermContext,i)


        def ADD(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.ADD)
            else:
                return self.getToken(SignalFlowV2Parser.ADD, i)

        def MINUS(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.MINUS)
            else:
                return self.getToken(SignalFlowV2Parser.MINUS, i)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_arith_expr

        def enterRule(self, listener):
            if hasattr(listener, "enterArith_expr"):
                listener.enterArith_expr(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitArith_expr"):
                listener.exitArith_expr(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitArith_expr"):
                return visitor.visitArith_expr(self)
            else:
                return visitor.visitChildren(self)




    def arith_expr(self):

        localctx = SignalFlowV2Parser.Arith_exprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 82, self.RULE_arith_expr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 437
            self.term()
            self.state = 442
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==SignalFlowV2Parser.ADD or _la==SignalFlowV2Parser.MINUS:
                self.state = 438
                _la = self._input.LA(1)
                if not(_la==SignalFlowV2Parser.ADD or _la==SignalFlowV2Parser.MINUS):
                    self._errHandler.recoverInline(self)
                else:
                    self.consume()
                self.state = 439
                self.term()
                self.state = 444
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class TermContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.TermContext, self).__init__(parent, invokingState)
            self.parser = parser

        def factor(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.FactorContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.FactorContext,i)


        def STAR(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.STAR)
            else:
                return self.getToken(SignalFlowV2Parser.STAR, i)

        def DIV(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.DIV)
            else:
                return self.getToken(SignalFlowV2Parser.DIV, i)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_term

        def enterRule(self, listener):
            if hasattr(listener, "enterTerm"):
                listener.enterTerm(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitTerm"):
                listener.exitTerm(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitTerm"):
                return visitor.visitTerm(self)
            else:
                return visitor.visitChildren(self)




    def term(self):

        localctx = SignalFlowV2Parser.TermContext(self, self._ctx, self.state)
        self.enterRule(localctx, 84, self.RULE_term)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 445
            self.factor()
            self.state = 450
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==SignalFlowV2Parser.STAR or _la==SignalFlowV2Parser.DIV:
                self.state = 446
                _la = self._input.LA(1)
                if not(_la==SignalFlowV2Parser.STAR or _la==SignalFlowV2Parser.DIV):
                    self._errHandler.recoverInline(self)
                else:
                    self.consume()
                self.state = 447
                self.factor()
                self.state = 452
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class FactorContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.FactorContext, self).__init__(parent, invokingState)
            self.parser = parser

        def factor(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.FactorContext,0)


        def ADD(self):
            return self.getToken(SignalFlowV2Parser.ADD, 0)

        def MINUS(self):
            return self.getToken(SignalFlowV2Parser.MINUS, 0)

        def NOT_OP(self):
            return self.getToken(SignalFlowV2Parser.NOT_OP, 0)

        def power(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.PowerContext,0)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_factor

        def enterRule(self, listener):
            if hasattr(listener, "enterFactor"):
                listener.enterFactor(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitFactor"):
                listener.exitFactor(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitFactor"):
                return visitor.visitFactor(self)
            else:
                return visitor.visitChildren(self)




    def factor(self):

        localctx = SignalFlowV2Parser.FactorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 86, self.RULE_factor)
        self._la = 0 # Token type
        try:
            self.state = 456
            token = self._input.LA(1)
            if token in [SignalFlowV2Parser.ADD, SignalFlowV2Parser.MINUS, SignalFlowV2Parser.NOT_OP]:
                self.enterOuterAlt(localctx, 1)
                self.state = 453
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << SignalFlowV2Parser.ADD) | (1 << SignalFlowV2Parser.MINUS) | (1 << SignalFlowV2Parser.NOT_OP))) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self.consume()
                self.state = 454
                self.factor()

            elif token in [SignalFlowV2Parser.NONE, SignalFlowV2Parser.TRUE, SignalFlowV2Parser.FALSE, SignalFlowV2Parser.ID, SignalFlowV2Parser.STRING, SignalFlowV2Parser.INT, SignalFlowV2Parser.FLOAT, SignalFlowV2Parser.OPEN_PAREN, SignalFlowV2Parser.OPEN_BRACK, SignalFlowV2Parser.OPEN_BRACE]:
                self.enterOuterAlt(localctx, 2)
                self.state = 455
                self.power()

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class PowerContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.PowerContext, self).__init__(parent, invokingState)
            self.parser = parser

        def atom_expr(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Atom_exprContext,0)


        def POWER(self):
            return self.getToken(SignalFlowV2Parser.POWER, 0)

        def factor(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.FactorContext,0)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_power

        def enterRule(self, listener):
            if hasattr(listener, "enterPower"):
                listener.enterPower(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitPower"):
                listener.exitPower(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitPower"):
                return visitor.visitPower(self)
            else:
                return visitor.visitChildren(self)




    def power(self):

        localctx = SignalFlowV2Parser.PowerContext(self, self._ctx, self.state)
        self.enterRule(localctx, 88, self.RULE_power)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 458
            self.atom_expr()
            self.state = 461
            _la = self._input.LA(1)
            if _la==SignalFlowV2Parser.POWER:
                self.state = 459
                self.match(SignalFlowV2Parser.POWER)
                self.state = 460
                self.factor()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Atom_exprContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Atom_exprContext, self).__init__(parent, invokingState)
            self.parser = parser

        def atom(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.AtomContext,0)


        def trailer(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.TrailerContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.TrailerContext,i)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_atom_expr

        def enterRule(self, listener):
            if hasattr(listener, "enterAtom_expr"):
                listener.enterAtom_expr(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitAtom_expr"):
                listener.exitAtom_expr(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitAtom_expr"):
                return visitor.visitAtom_expr(self)
            else:
                return visitor.visitChildren(self)




    def atom_expr(self):

        localctx = SignalFlowV2Parser.Atom_exprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 90, self.RULE_atom_expr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 463
            self.atom()
            self.state = 467
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << SignalFlowV2Parser.DOT) | (1 << SignalFlowV2Parser.OPEN_PAREN) | (1 << SignalFlowV2Parser.OPEN_BRACK))) != 0):
                self.state = 464
                self.trailer()
                self.state = 469
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class AtomContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.AtomContext, self).__init__(parent, invokingState)
            self.parser = parser

        def list_expr(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.List_exprContext,0)


        def tuple_expr(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Tuple_exprContext,0)


        def dict_expr(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Dict_exprContext,0)


        def ID(self):
            return self.getToken(SignalFlowV2Parser.ID, 0)

        def INT(self):
            return self.getToken(SignalFlowV2Parser.INT, 0)

        def FLOAT(self):
            return self.getToken(SignalFlowV2Parser.FLOAT, 0)

        def STRING(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.STRING)
            else:
                return self.getToken(SignalFlowV2Parser.STRING, i)

        def NONE(self):
            return self.getToken(SignalFlowV2Parser.NONE, 0)

        def TRUE(self):
            return self.getToken(SignalFlowV2Parser.TRUE, 0)

        def FALSE(self):
            return self.getToken(SignalFlowV2Parser.FALSE, 0)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_atom

        def enterRule(self, listener):
            if hasattr(listener, "enterAtom"):
                listener.enterAtom(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitAtom"):
                listener.exitAtom(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitAtom"):
                return visitor.visitAtom(self)
            else:
                return visitor.visitChildren(self)




    def atom(self):

        localctx = SignalFlowV2Parser.AtomContext(self, self._ctx, self.state)
        self.enterRule(localctx, 92, self.RULE_atom)
        self._la = 0 # Token type
        try:
            self.state = 484
            token = self._input.LA(1)
            if token in [SignalFlowV2Parser.OPEN_BRACK]:
                self.enterOuterAlt(localctx, 1)
                self.state = 470
                self.list_expr()

            elif token in [SignalFlowV2Parser.OPEN_PAREN]:
                self.enterOuterAlt(localctx, 2)
                self.state = 471
                self.tuple_expr()

            elif token in [SignalFlowV2Parser.OPEN_BRACE]:
                self.enterOuterAlt(localctx, 3)
                self.state = 472
                self.dict_expr()

            elif token in [SignalFlowV2Parser.ID]:
                self.enterOuterAlt(localctx, 4)
                self.state = 473
                self.match(SignalFlowV2Parser.ID)

            elif token in [SignalFlowV2Parser.INT]:
                self.enterOuterAlt(localctx, 5)
                self.state = 474
                self.match(SignalFlowV2Parser.INT)

            elif token in [SignalFlowV2Parser.FLOAT]:
                self.enterOuterAlt(localctx, 6)
                self.state = 475
                self.match(SignalFlowV2Parser.FLOAT)

            elif token in [SignalFlowV2Parser.STRING]:
                self.enterOuterAlt(localctx, 7)
                self.state = 477 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 476
                    self.match(SignalFlowV2Parser.STRING)
                    self.state = 479 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==SignalFlowV2Parser.STRING):
                        break


            elif token in [SignalFlowV2Parser.NONE]:
                self.enterOuterAlt(localctx, 8)
                self.state = 481
                self.match(SignalFlowV2Parser.NONE)

            elif token in [SignalFlowV2Parser.TRUE]:
                self.enterOuterAlt(localctx, 9)
                self.state = 482
                self.match(SignalFlowV2Parser.TRUE)

            elif token in [SignalFlowV2Parser.FALSE]:
                self.enterOuterAlt(localctx, 10)
                self.state = 483
                self.match(SignalFlowV2Parser.FALSE)

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class TrailerContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.TrailerContext, self).__init__(parent, invokingState)
            self.parser = parser

        def OPEN_PAREN(self):
            return self.getToken(SignalFlowV2Parser.OPEN_PAREN, 0)

        def CLOSE_PAREN(self):
            return self.getToken(SignalFlowV2Parser.CLOSE_PAREN, 0)

        def actual_args(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Actual_argsContext,0)


        def OPEN_BRACK(self):
            return self.getToken(SignalFlowV2Parser.OPEN_BRACK, 0)

        def subscript(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.SubscriptContext,0)


        def CLOSE_BRACK(self):
            return self.getToken(SignalFlowV2Parser.CLOSE_BRACK, 0)

        def DOT(self):
            return self.getToken(SignalFlowV2Parser.DOT, 0)

        def ID(self):
            return self.getToken(SignalFlowV2Parser.ID, 0)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_trailer

        def enterRule(self, listener):
            if hasattr(listener, "enterTrailer"):
                listener.enterTrailer(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitTrailer"):
                listener.exitTrailer(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitTrailer"):
                return visitor.visitTrailer(self)
            else:
                return visitor.visitChildren(self)




    def trailer(self):

        localctx = SignalFlowV2Parser.TrailerContext(self, self._ctx, self.state)
        self.enterRule(localctx, 94, self.RULE_trailer)
        self._la = 0 # Token type
        try:
            self.state = 497
            token = self._input.LA(1)
            if token in [SignalFlowV2Parser.OPEN_PAREN]:
                self.enterOuterAlt(localctx, 1)
                self.state = 486
                self.match(SignalFlowV2Parser.OPEN_PAREN)
                self.state = 488
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << SignalFlowV2Parser.LAMBDA) | (1 << SignalFlowV2Parser.NOT) | (1 << SignalFlowV2Parser.NONE) | (1 << SignalFlowV2Parser.TRUE) | (1 << SignalFlowV2Parser.FALSE) | (1 << SignalFlowV2Parser.ID) | (1 << SignalFlowV2Parser.STRING) | (1 << SignalFlowV2Parser.INT) | (1 << SignalFlowV2Parser.FLOAT) | (1 << SignalFlowV2Parser.STAR) | (1 << SignalFlowV2Parser.OPEN_PAREN) | (1 << SignalFlowV2Parser.POWER) | (1 << SignalFlowV2Parser.OPEN_BRACK) | (1 << SignalFlowV2Parser.ADD) | (1 << SignalFlowV2Parser.MINUS) | (1 << SignalFlowV2Parser.NOT_OP) | (1 << SignalFlowV2Parser.OPEN_BRACE))) != 0):
                    self.state = 487
                    self.actual_args()


                self.state = 490
                self.match(SignalFlowV2Parser.CLOSE_PAREN)

            elif token in [SignalFlowV2Parser.OPEN_BRACK]:
                self.enterOuterAlt(localctx, 2)
                self.state = 491
                self.match(SignalFlowV2Parser.OPEN_BRACK)
                self.state = 492
                self.subscript()
                self.state = 493
                self.match(SignalFlowV2Parser.CLOSE_BRACK)

            elif token in [SignalFlowV2Parser.DOT]:
                self.enterOuterAlt(localctx, 3)
                self.state = 495
                self.match(SignalFlowV2Parser.DOT)
                self.state = 496
                self.match(SignalFlowV2Parser.ID)

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class SubscriptContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.SubscriptContext, self).__init__(parent, invokingState)
            self.parser = parser

        def test(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.TestContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.TestContext,i)


        def COLON(self):
            return self.getToken(SignalFlowV2Parser.COLON, 0)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_subscript

        def enterRule(self, listener):
            if hasattr(listener, "enterSubscript"):
                listener.enterSubscript(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitSubscript"):
                listener.exitSubscript(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitSubscript"):
                return visitor.visitSubscript(self)
            else:
                return visitor.visitChildren(self)




    def subscript(self):

        localctx = SignalFlowV2Parser.SubscriptContext(self, self._ctx, self.state)
        self.enterRule(localctx, 96, self.RULE_subscript)
        self._la = 0 # Token type
        try:
            self.state = 507
            self._errHandler.sync(self);
            la_ = self._interp.adaptivePredict(self._input,59,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 499
                self.test()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 501
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << SignalFlowV2Parser.LAMBDA) | (1 << SignalFlowV2Parser.NOT) | (1 << SignalFlowV2Parser.NONE) | (1 << SignalFlowV2Parser.TRUE) | (1 << SignalFlowV2Parser.FALSE) | (1 << SignalFlowV2Parser.ID) | (1 << SignalFlowV2Parser.STRING) | (1 << SignalFlowV2Parser.INT) | (1 << SignalFlowV2Parser.FLOAT) | (1 << SignalFlowV2Parser.OPEN_PAREN) | (1 << SignalFlowV2Parser.OPEN_BRACK) | (1 << SignalFlowV2Parser.ADD) | (1 << SignalFlowV2Parser.MINUS) | (1 << SignalFlowV2Parser.NOT_OP) | (1 << SignalFlowV2Parser.OPEN_BRACE))) != 0):
                    self.state = 500
                    self.test()


                self.state = 503
                self.match(SignalFlowV2Parser.COLON)
                self.state = 505
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << SignalFlowV2Parser.LAMBDA) | (1 << SignalFlowV2Parser.NOT) | (1 << SignalFlowV2Parser.NONE) | (1 << SignalFlowV2Parser.TRUE) | (1 << SignalFlowV2Parser.FALSE) | (1 << SignalFlowV2Parser.ID) | (1 << SignalFlowV2Parser.STRING) | (1 << SignalFlowV2Parser.INT) | (1 << SignalFlowV2Parser.FLOAT) | (1 << SignalFlowV2Parser.OPEN_PAREN) | (1 << SignalFlowV2Parser.OPEN_BRACK) | (1 << SignalFlowV2Parser.ADD) | (1 << SignalFlowV2Parser.MINUS) | (1 << SignalFlowV2Parser.NOT_OP) | (1 << SignalFlowV2Parser.OPEN_BRACE))) != 0):
                    self.state = 504
                    self.test()


                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class List_exprContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.List_exprContext, self).__init__(parent, invokingState)
            self.parser = parser

        def OPEN_BRACK(self):
            return self.getToken(SignalFlowV2Parser.OPEN_BRACK, 0)

        def CLOSE_BRACK(self):
            return self.getToken(SignalFlowV2Parser.CLOSE_BRACK, 0)

        def test(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.TestContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.TestContext,i)


        def COMMA(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.COMMA)
            else:
                return self.getToken(SignalFlowV2Parser.COMMA, i)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_list_expr

        def enterRule(self, listener):
            if hasattr(listener, "enterList_expr"):
                listener.enterList_expr(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitList_expr"):
                listener.exitList_expr(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitList_expr"):
                return visitor.visitList_expr(self)
            else:
                return visitor.visitChildren(self)




    def list_expr(self):

        localctx = SignalFlowV2Parser.List_exprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 98, self.RULE_list_expr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 509
            self.match(SignalFlowV2Parser.OPEN_BRACK)
            self.state = 518
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << SignalFlowV2Parser.LAMBDA) | (1 << SignalFlowV2Parser.NOT) | (1 << SignalFlowV2Parser.NONE) | (1 << SignalFlowV2Parser.TRUE) | (1 << SignalFlowV2Parser.FALSE) | (1 << SignalFlowV2Parser.ID) | (1 << SignalFlowV2Parser.STRING) | (1 << SignalFlowV2Parser.INT) | (1 << SignalFlowV2Parser.FLOAT) | (1 << SignalFlowV2Parser.OPEN_PAREN) | (1 << SignalFlowV2Parser.OPEN_BRACK) | (1 << SignalFlowV2Parser.ADD) | (1 << SignalFlowV2Parser.MINUS) | (1 << SignalFlowV2Parser.NOT_OP) | (1 << SignalFlowV2Parser.OPEN_BRACE))) != 0):
                self.state = 510
                self.test()
                self.state = 515
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==SignalFlowV2Parser.COMMA:
                    self.state = 511
                    self.match(SignalFlowV2Parser.COMMA)
                    self.state = 512
                    self.test()
                    self.state = 517
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



            self.state = 520
            self.match(SignalFlowV2Parser.CLOSE_BRACK)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Tuple_exprContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Tuple_exprContext, self).__init__(parent, invokingState)
            self.parser = parser

        def OPEN_PAREN(self):
            return self.getToken(SignalFlowV2Parser.OPEN_PAREN, 0)

        def CLOSE_PAREN(self):
            return self.getToken(SignalFlowV2Parser.CLOSE_PAREN, 0)

        def testlist(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.TestlistContext,0)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_tuple_expr

        def enterRule(self, listener):
            if hasattr(listener, "enterTuple_expr"):
                listener.enterTuple_expr(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitTuple_expr"):
                listener.exitTuple_expr(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitTuple_expr"):
                return visitor.visitTuple_expr(self)
            else:
                return visitor.visitChildren(self)




    def tuple_expr(self):

        localctx = SignalFlowV2Parser.Tuple_exprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 100, self.RULE_tuple_expr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 522
            self.match(SignalFlowV2Parser.OPEN_PAREN)
            self.state = 524
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << SignalFlowV2Parser.LAMBDA) | (1 << SignalFlowV2Parser.NOT) | (1 << SignalFlowV2Parser.NONE) | (1 << SignalFlowV2Parser.TRUE) | (1 << SignalFlowV2Parser.FALSE) | (1 << SignalFlowV2Parser.ID) | (1 << SignalFlowV2Parser.STRING) | (1 << SignalFlowV2Parser.INT) | (1 << SignalFlowV2Parser.FLOAT) | (1 << SignalFlowV2Parser.OPEN_PAREN) | (1 << SignalFlowV2Parser.OPEN_BRACK) | (1 << SignalFlowV2Parser.ADD) | (1 << SignalFlowV2Parser.MINUS) | (1 << SignalFlowV2Parser.NOT_OP) | (1 << SignalFlowV2Parser.OPEN_BRACE))) != 0):
                self.state = 523
                self.testlist()


            self.state = 526
            self.match(SignalFlowV2Parser.CLOSE_PAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Dict_exprContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Dict_exprContext, self).__init__(parent, invokingState)
            self.parser = parser

        def OPEN_BRACE(self):
            return self.getToken(SignalFlowV2Parser.OPEN_BRACE, 0)

        def CLOSE_BRACE(self):
            return self.getToken(SignalFlowV2Parser.CLOSE_BRACE, 0)

        def test(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.TestContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.TestContext,i)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_dict_expr

        def enterRule(self, listener):
            if hasattr(listener, "enterDict_expr"):
                listener.enterDict_expr(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitDict_expr"):
                listener.exitDict_expr(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitDict_expr"):
                return visitor.visitDict_expr(self)
            else:
                return visitor.visitChildren(self)




    def dict_expr(self):

        localctx = SignalFlowV2Parser.Dict_exprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 102, self.RULE_dict_expr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 528
            self.match(SignalFlowV2Parser.OPEN_BRACE)
            self.state = 545
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << SignalFlowV2Parser.LAMBDA) | (1 << SignalFlowV2Parser.NOT) | (1 << SignalFlowV2Parser.NONE) | (1 << SignalFlowV2Parser.TRUE) | (1 << SignalFlowV2Parser.FALSE) | (1 << SignalFlowV2Parser.ID) | (1 << SignalFlowV2Parser.STRING) | (1 << SignalFlowV2Parser.INT) | (1 << SignalFlowV2Parser.FLOAT) | (1 << SignalFlowV2Parser.OPEN_PAREN) | (1 << SignalFlowV2Parser.OPEN_BRACK) | (1 << SignalFlowV2Parser.ADD) | (1 << SignalFlowV2Parser.MINUS) | (1 << SignalFlowV2Parser.NOT_OP) | (1 << SignalFlowV2Parser.OPEN_BRACE))) != 0):
                self.state = 529
                self.test()
                self.state = 530
                self.match(SignalFlowV2Parser.COLON)
                self.state = 531
                self.test()
                self.state = 539
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,63,self._ctx)
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1:
                        self.state = 532
                        self.match(SignalFlowV2Parser.COMMA)
                        self.state = 533
                        self.test()
                        self.state = 534
                        self.match(SignalFlowV2Parser.COLON)
                        self.state = 535
                        self.test() 
                    self.state = 541
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,63,self._ctx)

                self.state = 543
                _la = self._input.LA(1)
                if _la==SignalFlowV2Parser.COMMA:
                    self.state = 542
                    self.match(SignalFlowV2Parser.COMMA)




            self.state = 547
            self.match(SignalFlowV2Parser.CLOSE_BRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class TestlistContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.TestlistContext, self).__init__(parent, invokingState)
            self.parser = parser

        def test(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.TestContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.TestContext,i)


        def COMMA(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.COMMA)
            else:
                return self.getToken(SignalFlowV2Parser.COMMA, i)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_testlist

        def enterRule(self, listener):
            if hasattr(listener, "enterTestlist"):
                listener.enterTestlist(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitTestlist"):
                listener.exitTestlist(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitTestlist"):
                return visitor.visitTestlist(self)
            else:
                return visitor.visitChildren(self)




    def testlist(self):

        localctx = SignalFlowV2Parser.TestlistContext(self, self._ctx, self.state)
        self.enterRule(localctx, 104, self.RULE_testlist)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 549
            self.test()
            self.state = 554
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,66,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 550
                    self.match(SignalFlowV2Parser.COMMA)
                    self.state = 551
                    self.test() 
                self.state = 556
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,66,self._ctx)

            self.state = 558
            _la = self._input.LA(1)
            if _la==SignalFlowV2Parser.COMMA:
                self.state = 557
                self.match(SignalFlowV2Parser.COMMA)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Actual_argsContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Actual_argsContext, self).__init__(parent, invokingState)
            self.parser = parser

        def argument(self, i=None):
            if i is None:
                return self.getTypedRuleContexts(SignalFlowV2Parser.ArgumentContext)
            else:
                return self.getTypedRuleContext(SignalFlowV2Parser.ArgumentContext,i)


        def actual_star_arg(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Actual_star_argContext,0)


        def actual_kws_arg(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.Actual_kws_argContext,0)


        def COMMA(self, i=None):
            if i is None:
                return self.getTokens(SignalFlowV2Parser.COMMA)
            else:
                return self.getToken(SignalFlowV2Parser.COMMA, i)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_actual_args

        def enterRule(self, listener):
            if hasattr(listener, "enterActual_args"):
                listener.enterActual_args(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitActual_args"):
                listener.exitActual_args(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitActual_args"):
                return visitor.visitActual_args(self)
            else:
                return visitor.visitChildren(self)




    def actual_args(self):

        localctx = SignalFlowV2Parser.Actual_argsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 106, self.RULE_actual_args)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 565
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,68,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 560
                    self.argument()
                    self.state = 561
                    self.match(SignalFlowV2Parser.COMMA) 
                self.state = 567
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,68,self._ctx)

            self.state = 585
            token = self._input.LA(1)
            if token in [SignalFlowV2Parser.LAMBDA, SignalFlowV2Parser.NOT, SignalFlowV2Parser.NONE, SignalFlowV2Parser.TRUE, SignalFlowV2Parser.FALSE, SignalFlowV2Parser.ID, SignalFlowV2Parser.STRING, SignalFlowV2Parser.INT, SignalFlowV2Parser.FLOAT, SignalFlowV2Parser.OPEN_PAREN, SignalFlowV2Parser.OPEN_BRACK, SignalFlowV2Parser.ADD, SignalFlowV2Parser.MINUS, SignalFlowV2Parser.NOT_OP, SignalFlowV2Parser.OPEN_BRACE]:
                self.state = 568
                self.argument()
                self.state = 570
                _la = self._input.LA(1)
                if _la==SignalFlowV2Parser.COMMA:
                    self.state = 569
                    self.match(SignalFlowV2Parser.COMMA)



            elif token in [SignalFlowV2Parser.STAR]:
                self.state = 572
                self.actual_star_arg()
                self.state = 577
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,70,self._ctx)
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1:
                        self.state = 573
                        self.match(SignalFlowV2Parser.COMMA)
                        self.state = 574
                        self.argument() 
                    self.state = 579
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,70,self._ctx)

                self.state = 582
                _la = self._input.LA(1)
                if _la==SignalFlowV2Parser.COMMA:
                    self.state = 580
                    self.match(SignalFlowV2Parser.COMMA)
                    self.state = 581
                    self.actual_kws_arg()



            elif token in [SignalFlowV2Parser.POWER]:
                self.state = 584
                self.actual_kws_arg()

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Actual_star_argContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Actual_star_argContext, self).__init__(parent, invokingState)
            self.parser = parser

        def STAR(self):
            return self.getToken(SignalFlowV2Parser.STAR, 0)

        def test(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.TestContext,0)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_actual_star_arg

        def enterRule(self, listener):
            if hasattr(listener, "enterActual_star_arg"):
                listener.enterActual_star_arg(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitActual_star_arg"):
                listener.exitActual_star_arg(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitActual_star_arg"):
                return visitor.visitActual_star_arg(self)
            else:
                return visitor.visitChildren(self)




    def actual_star_arg(self):

        localctx = SignalFlowV2Parser.Actual_star_argContext(self, self._ctx, self.state)
        self.enterRule(localctx, 108, self.RULE_actual_star_arg)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 587
            self.match(SignalFlowV2Parser.STAR)
            self.state = 588
            self.test()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Actual_kws_argContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.Actual_kws_argContext, self).__init__(parent, invokingState)
            self.parser = parser

        def POWER(self):
            return self.getToken(SignalFlowV2Parser.POWER, 0)

        def test(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.TestContext,0)


        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_actual_kws_arg

        def enterRule(self, listener):
            if hasattr(listener, "enterActual_kws_arg"):
                listener.enterActual_kws_arg(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitActual_kws_arg"):
                listener.exitActual_kws_arg(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitActual_kws_arg"):
                return visitor.visitActual_kws_arg(self)
            else:
                return visitor.visitChildren(self)




    def actual_kws_arg(self):

        localctx = SignalFlowV2Parser.Actual_kws_argContext(self, self._ctx, self.state)
        self.enterRule(localctx, 110, self.RULE_actual_kws_arg)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 590
            self.match(SignalFlowV2Parser.POWER)
            self.state = 591
            self.test()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ArgumentContext(ParserRuleContext):

        def __init__(self, parser, parent=None, invokingState=-1):
            super(SignalFlowV2Parser.ArgumentContext, self).__init__(parent, invokingState)
            self.parser = parser

        def test(self):
            return self.getTypedRuleContext(SignalFlowV2Parser.TestContext,0)


        def ID(self):
            return self.getToken(SignalFlowV2Parser.ID, 0)

        def ASSIGN(self):
            return self.getToken(SignalFlowV2Parser.ASSIGN, 0)

        def getRuleIndex(self):
            return SignalFlowV2Parser.RULE_argument

        def enterRule(self, listener):
            if hasattr(listener, "enterArgument"):
                listener.enterArgument(self)

        def exitRule(self, listener):
            if hasattr(listener, "exitArgument"):
                listener.exitArgument(self)

        def accept(self, visitor):
            if hasattr(visitor, "visitArgument"):
                return visitor.visitArgument(self)
            else:
                return visitor.visitChildren(self)




    def argument(self):

        localctx = SignalFlowV2Parser.ArgumentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 112, self.RULE_argument)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 595
            self._errHandler.sync(self);
            la_ = self._interp.adaptivePredict(self._input,73,self._ctx)
            if la_ == 1:
                self.state = 593
                self.match(SignalFlowV2Parser.ID)
                self.state = 594
                self.match(SignalFlowV2Parser.ASSIGN)


            self.state = 597
            self.test()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





