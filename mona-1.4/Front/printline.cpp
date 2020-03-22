/*
 * MONA
 * Copyright (C) 1997-2013 Aarhus University.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the  Free Software
 * Foundation, Inc., 51 Franklin Street, Suite 500, Boston, MA 02110-1335,
 * USA.
 */

#include <string.h>
#include <iostream>

#include "printline.h"

using std::cout;

Pos dummyPos;

extern Deque<FileSource *> source;
extern Deque<char *> fileNames;

void 
Pos::printsource()
{
  char *str;
  int c;
  size_t t;
  char temp[77];

  if (line == -1)
    return;

  for (t = 0; t < fileNames.size(); t++)
    if (fileName == fileNames.get(t))
      break;
  cout << " '" << fileName << "' line " << line << " column " << col << "\n"; 
  str = source.get(t)->get(line-1);

  c = col;
  if (strlen(str) >= 73) {
    if (col > 73) {
      for (t = 0; t < 76; t++) {
	if (str[col - 40 + t] != '\0')
	  temp[t] = str[col - 40 + t];
	else
	  break;
      }
      temp[t] = '\0';
      c = 40;
    }
    else {
      strncpy(temp, str, 77);
      temp[76] = '\0';
    }
  }
  else
    strcpy(temp, str);
  cout << "  " << temp << "\n  ";
  if (c < 77) {
    for (t = 1; t < (size_t)c; t++)
      if (t < strlen(temp) && temp[t] == '\t')
        cout << "\t";
      else
        cout << " ";
    cout << "^";
  } 
}
