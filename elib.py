
from modules.func import *

reponame = "euda"

repopath = Path(__file__).resolve().parents[0]
repotitle = os.path.basename(repopath)
snapdir = repopath / "_snapshot"
execdir = Path().absolute()  # Get the folder script is executed in

projname, projdir = None, None

for i, d in enumerate(execdir.parents):
    if d.stem == "src":
        projname = execdir.parts[-i-1]
        projdir = Path(*execdir.parts[:-i])

if projname != None:
    datadir = projdir / "_data"
    rawdir = datadir / "raw"
    intermdir = datadir / "interm"
    outputdir = datadir / "output"
    vizdir = projdir / "viz"

ignoredirs = ["_data", "viz", "examples"]


def runstartup():
    snapshot(scheduled=True)
    return starttimer()


def runinit():
    mkdirpy(datadir)
    mkdirpy(rawdir)
    mkdirpy(intermdir)
    mkdirpy(vizdir)
    mkdirpy(outputdir)
    mkdirpy(snapdir)


def snapshot(description="manual", scheduled=False):
    """(description, scheduled) Copy scripts to snapshot if there isn't one for this week already,
    and files have been changed"""
    print("...Checking snapshots...")

    if not os.path.exists(snapdir):
        raise ValueError("_snapshot folder does not exist in project parent dir!")
    if not os.path.exists(snapdir / projname):
        mkdirpy(snapdir / projname)

    snapshots = os.listdir(snapdir / projname)
    mostrecent = datetime.date(2000, 1, 1)
    for d in snapshots:
        if len(d) != 10:  # Ignore manual snapshots
            continue
        dtime = datetime.datetime.strptime(d, "%Y-%m-%d").date()
        if dtime > mostrecent:
            mostrecent = dtime

    cmpdirs = []
    checkdirs = []
    difffiles = []
    difffiledirs = []
    newfiles = []

    for path, dirs, files in os.walk(projdir):
        p = Path(path)
        if len(set.intersection(set(p.parts), set(ignoredirs))) == 0:
            if p != projdir:
                cmpdirs.append(p)
                diff = [item for item in p.parts if item not in projdir.parts]
                checkdir = snapdir / projname / str(mostrecent)
                for part in diff: checkdir = checkdir.joinpath(part)
                checkdirs.append(checkdir)

    for sourcedir, checkdir in zip(cmpdirs, checkdirs):
        if not checkdir.exists():
            newfiles += os.listdir(sourcedir)
            continue
        diffs = dircmp(sourcedir, checkdir).diff_files
        difffiles = difffiles + diffs
        difffiledirs += [sourcedir] * len(diffs)
        newfiles = newfiles + dircmp(sourcedir, checkdir).left_only

    destname = str(datetime.date.today())
    if not scheduled:
        destname = destname + " - " + description
    if scheduled:
        delta = (datetime.date.today() - mostrecent).days
        if len(difffiles + newfiles) == 0 or delta < 7:
            # Don't snapshot if no files have been modified or it has been less than 1 week since
            return None

    print("Saving snapshot...")
    destdir = snapdir / projname / destname
    for d in os.listdir(projdir):
        if d not in ignoredirs:
            copytree(projdir / d, destdir / d)
    #copytree(projdir, destdir, ignore=copytreeignoredirs)

    for f, d in zip(difffiles, difffiledirs):
        diff = [item for item in d.parts if item not in projdir.parts]
        fname = os.path.splitext(f)[0] + ".diff"
        new = snapdir / projname / destname
        for part in diff:
            new = new.joinpath(part)
        p = Path(new, fname)
        p.touch()


def writeinterm(filename, data, inparallel=False):
    """Dump data into pickle file in path"""
    filename += ".pkl"
    filepath = intermdir
    if inparallel:
        filepath = intermdir / "_parallel-stores"
    mkdirpy(filepath)
    file = filepath / filename
    potentialrename = True
    #dirlist = os.scandir(intermdir)
    with open(file, 'wb') as pickle_file:
        pickle.dump(data, pickle_file)
    # Check if there are identical files
    if potentialrename:
        for f in os.scandir(filepath):
            if f.is_file():
                filename2 = os.path.basename(f)
                if filename2 != filename:
                    if comparefiles(file, filepath / f):
                        print("Renaming file: " + filename2)
                        os.remove(filepath / f)
    print(f"-> {humanize.naturalsize(os.path.getsize(file))}")


def loadinterm(filename):
    """Return data from pickle file in path"""
    filename += ".pkl"
    filepath = intermdir
    file = filepath / filename
    with open(file, 'rb') as pickle_file:
        data = pickle.load(pickle_file)
    return data


def toexcel(data, filename, sheets, keepindex=False):
    """(data, filename, sheets, final=False, keepindex=False)
    Export data to .xlsx file. Pass pandas dataframe,
    or dict of data for sheets=True."""

    savepath = intermdir
    mkdirpy(savepath)
    excelfile = filename + ".xlsx"
    potentialrename = True
    dirlist = os.scandir(savepath)
    for f in dirlist:
        if f.is_file():
            filename2 = os.path.basename(f)
            if filename2 == excelfile:
                potentialrename = False

    if sheets:
        with pd.ExcelWriter(savepath / excelfile) as writer:
            for k, v in data.items():
                v.to_excel(writer, sheet_name=k, index=keepindex)
    else:
        with pd.ExcelWriter(savepath / excelfile) as writer:
            data.to_excel(writer, index=keepindex)
    # Check if the file is a rename
    if potentialrename:
        for f in os.scandir(savepath):
            if f.is_file():
                filename2 = os.path.basename(f)
                if filename2 != excelfile:
                    if os.path.splitext(filename2)[-1] == ".xlsx":
                        if compareexcels(savepath / excelfile, savepath / f):
                            print("Renaming file: " + filename2)
                            os.remove(savepath / filename2)



def main():
    pass


if __name__ == "__main__":
    main()

