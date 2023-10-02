BEGIN {
        printf(";\n");
        printf("; USAGE: awk -f (thisfile) (cell placement file)\n");
        printf(";\n");

        GRID = 0.375 / 2;
        RSFQ_CELLLIB_NAME = "\"adp619\""

        addCell("jtl", 1,1);
        addCell("jtl45deg", 1,2);
        addCell("jtl45degc", 1,2);
        addCell("jtl45degcc", 1,2);
        addCell("jtl45degccr", 1,2);
        addCell("jtl45degcr", 1,2);
        addCell("jtl45degrc", 1,2);
        addCell("jtl45degrcc", 1,2);
        addCell("jtl45degrccr", 1,2);
        addCell("jtl45degrcr", 1,2);

        addCell("jtlc", 1,1);
        addCell("jtlc2", 2,1);
        addCell("jtlc3", 2,1);

        addCell("jtlcc", 1,1);
        addCell("jtlccla", 2,1);
        addCell("jtlcclar",2,1);
        addCell("jtlccls", 2,1);

        addCell("jtlcclx1", 2,1);
        addCell("jtlcclx2", 2,1);
        addCell("jtlcclx3", 2,1);
        addCell("jtlcclx4", 2,1);
        addCell("jtlcclx5", 2,1);
        addCell("jtlcclx6", 2,1);
        addCell("jtlcclx7", 2,1);
        addCell("jtlcclx8", 2,1);
        addCell("jtlcclx9", 2,1);
        addCell("jtlcclx10", 2,1);
        addCell("jtlcclx11", 2,1);
        addCell("jtlcclx12", 2,1);

        addCell("jtlccr", 1,1);
        addCell("jtlccrla", 2,1);
        addCell("jtlccrlar",2,1);
        addCell("jtlccrls", 2,1);
        addCell("jtlccrlsr",2,1);

        addCell("jtlccx1", 2,1);
        addCell("jtlccx2", 2,1);
        addCell("jtlccx3", 2,1);

        addCell("jtlcx1", 2,1);
        addCell("jtlcx2", 2,1);
        addCell("jtlcx3", 2,1);
        addCell("jtlcx4", 2,1);
        addCell("jtlcx5", 2,1);
        addCell("jtlcx6", 2,1);
        addCell("jtlcx7", 2,1);
        addCell("jtlcx8", 2,1);

        addCell("jtlcxcx1", 2,2);
        addCell("jtllx1",   2,1);
        addCell("jtllx2",   2,1);
        addCell("jtlu",     1,2);
        addCell("jtluc",    1,2);

        addCell("jtluc2",  1,2);
        addCell("jtluc2r", 1,2);
        addCell("jtlucc1", 1,2);
        addCell("jtlucc2", 1,2);
        addCell("jtlucc3", 1,2);
        addCell("jtlucc4", 1,2);

        addCell("jtlucr",  1,2);
        addCell("jtlucx1", 1,2);
        addCell("jtlucx2", 1,2);
        addCell("jtlucx3", 1,2);
        addCell("jtlucx4", 1,2);

        addCell("jtlul",    1, 2);
        addCell("jtlulr",   1, 2);
        addCell("jtlurc",   1, 2);
        addCell("jtlurc2",  1, 2);
        addCell("jtlurc2r", 1, 2);
        addCell("jtlurcr",  1, 2);
        addCell("jtluu",    1, 2);
        addCell("jtluul1",  1, 2);
        addCell("jtluul2",  1, 2);
        addCell("jtluul3",  1, 2);
        addCell("jtluur",   1, 2);

        addCell("jtlw1", 2, 2);
        addCell("jtlw2", 2, 2);
        addCell("jtlw4", 2, 2);
        addCell("jtlw5", 2, 2);

        addCell("jtlx",      1, 1);
        addCell("jtlx2",     1, 2);
        addCell("jtlx2r",    1, 2);
        addCell("jtlx2rx",   1, 2);
        addCell("jtlx2rxr",  1, 2);
        addCell("jtlx2x"  ,  1, 2);

        addCell("jtlx3",     2, 1);
        addCell("jtlx4",     2, 1);
        addCell("jtlx5",     2, 2);
        addCell("jtlx5c",    2, 2);
        addCell("jtlx6",     2, 2);
        addCell("jtlx6c",    2, 2);
        addCell("jtlx7",     2, 2);
        addCell("jtlx7c1",   2, 2);
        addCell("jtlx7c2",   2, 2);

        addCell("jtlxx1", 2, 1);
        addCell("jtlxx2", 2, 1);
        addCell("jtlxx3", 2, 2);
        addCell("jtlxx4", 2, 2);
        addCell("jtlxx5", 2, 2);
        addCell("jtlxx6", 2, 2);

        addCell("ljtl", 2,1);


        addCell("spl3",      1, 1)
        addCell("spl3b",     2, 1)
        addCell("spl3bjtlx", 2, 1)
        addCell("spl3c",     2, 1)
        addCell("spl3d",     2, 1)
        addCell("spl3f",     2, 1)
        addCell("spl3fjtlx", 2, 1)
        addCell("spl3g",     2, 1)
        addCell("spl3h",     2, 1)
        addCell("spl3i",     2, 1)
        addCell("spl3j",     2, 1)
        addCell("spl3k",     2, 1)
        addCell("spl3l",     2, 1)
        addCell("spl3m",     2, 1)
        addCell("spl3n",     2, 1)
        addCell("spl3o",     2, 1)
        addCell("spl3p",     2, 1)
        addCell("spl3q",     2, 1)
        addCell("spl3q",     2, 1)


        addCell("spll",         1, 1)
        addCell("spll2",        2, 1)
        addCell("spll2c1",      2, 1)
        addCell("spll2c2",      2, 1)
        addCell("spll2c2jtlc",  2, 1)
        addCell("spll2jtl45x" , 2, 1)
        addCell("spll2jtl45xr", 2, 1)
        addCell("spll3",        2, 1)
        addCell("spll3c1",      2, 1)
        addCell("spll3c1jtlc",  2, 1)
        addCell("spll3c1jtlcr", 2, 1)
        addCell("spll3c2",      2, 1)
        addCell("spll3jtl45x",  2, 1)
        addCell("spll3jtl45xr", 2, 1)

        addCell("spll4",        1, 2)
        addCell("spll4c1",      1, 2)
        addCell("spll4c1jtlx",  1, 2)
        addCell("spll4c1jtlxr", 1, 2)
        addCell("spll4c2",      1, 2)
        addCell("splljtlx",     2, 1)
        addCell("splljtlx2",    2, 1)
        addCell("splljtlx3",    2, 1)
        addCell("splljtlx4",    2, 1)
        addCell("splljtlx5",    2, 1)
        addCell("splljtlx6",    2, 1)

        addCell("splt",         1, 1)
        addCell("splt2",        2, 1)
        addCell("splt3",        1, 2)
        addCell("splt3c1",      1, 2)
        addCell("splt3c2",      1, 2)
        addCell("spltc1",       1, 2)
        addCell("spltjtlx",     2, 1)
        addCell("spltjtlx2",    2, 1)
        addCell("spltjtlx3",    2, 1)

        addCell("splw1",        2, 2)
        addCell("splw2",        2, 2)
        addCell("splw3",        2, 2)
        addCell("splw4",        2, 2)


        printf("scv = (geGetWindowCellView (hiGetCurrentWindow))\n\n");
}

function addCell(cellName, x, y){
    printf("master%s  = dbOpenCellViewByType(%s \"%s\"    \"symbol_p\")\n", 
            toupper(cellName), RSFQ_CELLLIB_NAME, cellName);
    sizex[cellName] = x;
    sizey[cellName] = y;
}

/^/ {
    type = $1;
    posx = $2+0;
    posy = $3+0;
    flip = ($4 == "False") ? 0 : 1;
    rot  = $5+0;

    offsetx = offsety = 0;
    offsetx = (flip==0 && rot==1) ?-0.5 +sizey[type]             : offsetx;
    offsetx = (flip==0 && rot==2) ?-0.5             +sizex[type] : offsetx;
    offsetx = (flip==1 && rot==2) ?-0.5             +sizex[type] : offsetx;
    offsetx = (flip==1 && rot==3) ?-0.5 +sizey[type]             : offsetx;

    offsety = (flip==0 && rot==2) ?-0.5 +sizey[type]             : offsety;
    offsety = (flip==0 && rot==3) ?-0.5 +           +sizex[type] : offsety;
    offsety = (flip==1 && rot==0) ?-0.5 +sizey[type]             : offsety;
    offsety = (flip==1 && rot==3) ?-0.5 +           +sizex[type] : offsety;


    printf("PutCell( scv master%s list(%f %f) \"%s%s\" )\n", 
        toupper(type), 
        (posx + offsetx) * 2*GRID,
        (posy + offsety) * 2*GRID,
        flip==0 ? "" : (rot>=2 ? "MY" : "MX"), 
        flip==0 ? "R" (rot*90) : ((rot%2 == 0) ? "" : "R" ((rot%2)*90)));
}
