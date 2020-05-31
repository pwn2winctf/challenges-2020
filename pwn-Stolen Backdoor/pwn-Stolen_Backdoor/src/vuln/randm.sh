#!/bin/bash

#auxiliary script to randomize emoji list

echo "#ifndef emojilib
#define emojilib
#include <wchar.h>
const wchar_t emojiLib[] ={
" > emojis.h
cat emojisorted.h | shuf >> emojis.h

echo "end"
sed '$ s/.$//' emojis.h

echo "};

#define LEN_LIB 13264

#endif
" >> emojis.h
