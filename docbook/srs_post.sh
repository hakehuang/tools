#this script do post process of the xls to plain test srs document
# to get rid of those no yes requirements
#./srs_post.sh <the plan text file> <oiutput>

if [ $# -lt 2 ]; then
echo "need specify the input and output file"
exit 0
fi

if [ -e $1 ]; then

#first mark the yes requirements
sed "s/yes$/QWERTY/" $1 > $2

#then mark the non-requirements
sed -i "/_0/!s/$/QWERTY/" $2

#then remove the not yes requirements
sed -i "/QWERTY/!d" $2


#last remove the QWERTY pad
sed -i "s/QWERTY$//" $2

echo "done"
fi
