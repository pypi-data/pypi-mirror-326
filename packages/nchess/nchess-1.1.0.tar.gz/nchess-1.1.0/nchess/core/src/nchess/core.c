#include "core.h"

const int NCH_ROW_TABLE[64] = {
    0, 0, 0, 0, 0, 0, 0, 0,
    1, 1, 1, 1, 1, 1, 1, 1,
    2, 2, 2, 2, 2, 2, 2, 2,
    3, 3, 3, 3, 3, 3, 3, 3,
    4, 4, 4, 4, 4, 4, 4, 4,
    5, 5, 5, 5, 5, 5, 5, 5,
    6, 6, 6, 6, 6, 6, 6, 6,
    7, 7, 7, 7, 7, 7, 7, 7,
};

const int NCH_COL_TABLE[64] = {
    0, 1, 2, 3, 4, 5, 6, 7,
    0, 1, 2, 3, 4, 5, 6, 7,
    0, 1, 2, 3, 4, 5, 6, 7,
    0, 1, 2, 3, 4, 5, 6, 7,
    0, 1, 2, 3, 4, 5, 6, 7,
    0, 1, 2, 3, 4, 5, 6, 7,
    0, 1, 2, 3, 4, 5, 6, 7,
    0, 1, 2, 3, 4, 5, 6, 7,
};

const uint64 NCH_DIAGONAL_MAIN[15] = {
    0x0000000000000001ull,
    0x0000000000000101ull,
    0x0000000000010204ull,
    0x0000000001020408ull,
    0x0000000102040810ull,
    0x0000010204081020ull,
    0x0001020408102040ull,
    0x0102040810204080ull,
    0x0204081020408000ull,
    0x0408102040800000ull,
    0x0810204080000000ull,
    0x1020408000000000ull,
    0x2040800000000000ull,
    0x4080000000000000ull,
    0x8000000000000000ull,
};

const int NCH_DIAGONAL_MAIN_IDX[64] = {
    0, 1, 2, 3, 4, 5, 6, 7,
    1, 2, 3, 4, 5, 6, 7, 8,
    2, 3, 4, 5, 6, 7, 8, 9,
    3, 4, 5, 6, 7, 8, 9, 10,
    4, 5, 6, 7, 8, 9, 10, 11,
    5, 6, 7, 8, 9, 10, 11, 12,
    6, 7, 8, 9, 10, 11, 12, 13,
    7, 8, 9, 10, 11, 12, 13, 14
};

const uint64 NCH_DIAGONAL_ANTI[15] = {
    0x0000000000000080ull,
    0x0000000000008040ull,
    0x0000000000804020ull,
    0x0000000080402010ull,
    0x0000008040201008ull,
    
    0x0000804020100804ull,
    
    0x0080402010080402ull,
    0x8040201008040201ull,
    0x4020100804020100ull,
    0x2010080402010000ull,
    0x1008040201000000ull,
    0x0804020100000000ull,
    0x0402010000000000ull,
    0x0201000000000000ull,
    0x0100000000000000ull,
};

const int NCH_DIAGONAL_ANTI_IDX[64] = {
    7, 6, 5, 4, 3, 2, 1, 0,
    8, 7, 6, 5, 4, 3, 2, 1,
    9, 8, 7, 6, 5, 4, 3, 2,
    10, 9, 8, 7, 6, 5, 4, 3,
    11, 10, 9, 8, 7, 6, 5, 4,
    12, 11, 10, 9, 8, 7, 6, 5,
    13, 12, 11, 10, 9, 8, 7, 6,
    14, 13, 12, 11, 10, 9, 8, 7
};

Diractions NCH_DIRACTION_TABLE[NCH_SQUARE_NB][NCH_SQUARE_NB];

NCH_STATIC void
init_diractions(){
    int row, main, anti, cur, temp;
    for (int i = 0; i < NCH_SQUARE_NB; i++){

        for (int j = 0; j < NCH_SQUARE_NB; j++)
            NCH_DIRACTION_TABLE[i][j] = NCH_NO_DIR;
        
        row = NCH_GET_ROWIDX(i);
        main = NCH_GET_DIGMAINIDX(i);
        anti = NCH_GET_DIGANTIIDX(i);

        cur = i + 8;
        while (cur < 64)
        {
            NCH_DIRACTION_TABLE[i][cur] = NCH_Up;
            cur += 8;
        }
        
        cur = i - 8;
        while (cur >= 0)
        {
            NCH_DIRACTION_TABLE[i][cur] = NCH_Down;
            cur -= 8;
        }
        
        cur = i + 1;
        temp = NCH_GET_ROWIDX(cur);
        while (cur < 64 && temp == row)
        {
            NCH_DIRACTION_TABLE[i][cur] = NCH_Left;
            cur += 1;
            temp = NCH_GET_ROWIDX(cur);
        }
        
        cur = i - 1;
        temp = NCH_GET_ROWIDX(cur);
        while (cur > 0 && temp == row)
        {
            NCH_DIRACTION_TABLE[i][cur] = NCH_Right;
            cur -= 1;
            temp = NCH_GET_ROWIDX(cur);
        }

        cur = i + 7;
        temp = NCH_GET_DIGMAINIDX(cur);
        while (cur < 64 && temp == main)
        {
            NCH_DIRACTION_TABLE[i][cur] = NCH_UpRight;
            cur += 7;
            temp = NCH_GET_DIGMAINIDX(cur);
        }

        cur = i - 7;
        temp = NCH_GET_DIGMAINIDX(cur);
        while (cur > 0 && temp == main)
        {
            NCH_DIRACTION_TABLE[i][cur] = NCH_DownLeft;
            cur -= 7;
            temp = NCH_GET_DIGMAINIDX(cur);
        }

        cur = i - 9;
        temp = NCH_GET_DIGANTIIDX(cur);
        while (cur > 0 && temp == anti)
        {
            NCH_DIRACTION_TABLE[i][cur] = NCH_DownRight;
            cur -= 9;
            temp = NCH_GET_DIGANTIIDX(cur);
        }

        cur = i + 9;
        temp = NCH_GET_DIGANTIIDX(cur);
        while (cur < 64 && temp == anti)
        {
            NCH_DIRACTION_TABLE[i][cur] = NCH_UpLeft;
            cur += 9;
            temp = NCH_GET_DIGANTIIDX(cur);
        }
    }
}

void
NCH_InitTables(){
    init_diractions();
}
