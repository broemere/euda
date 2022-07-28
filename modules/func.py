
from modules.headers import *

def mkdirpy(path):
    """Creates directory if it doesn't exist"""
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

class starttimer:
    def __init__(self):
        self.t0 = perf_counter()
        self.tx = 0

    def check(self, minutes=False):
        """Return time since last check (or start if first check)
        Default seconds
        Pass True to return minutes
        """
        self.appendage = " sec"
        if self.tx == 0:
            self.tx = perf_counter()
            self.t_out = self.tx - self.t0
        else:
            self.tx2 = perf_counter()
            self.t_out = self.tx2 - self.tx
            self.tx = self.tx2
        if minutes:
            self.t_out = self.t_out / 60
            self.appendage = " min"
        #return str(int(self.t_out)) + self.appendage + "\n"
        print(str(int(self.t_out)) + self.appendage + "\n")

    def total(self, minutes=False):
        """Return time since start
        Default seconds
        Pass True for minutes
        """
        self.appendage = " sec"
        self.t_out = perf_counter() - self.t0
        if minutes:
            self.t_out = self.t_out / 60
            self.appendage = " min"
        #return str(int(self.t_out)) + self.appendage + "\n"
        print(str(int(self.t_out)) + self.appendage + "\n")


def display(img, gray=False):
    fig = plt.figure(dpi=300, frameon=False)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    if gray:
        ax.imshow(img, cmap="gray")
    else:
        ax.imshow(img)
    plt.show()
    plt.close()


def graph(x, y, xlabel="", ylabel="", title="", file=""):
    plt.figure(dpi=300)
    plt.scatter(x, y, marker=".")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    if file != "":
        d = os.path.dirname(file)
        mkdirpy(d)
        plt.savefig(str(file))
        plt.close()
        #cv2.imwrite(str(file), plt)
    else:
        plt.show()
        plt.close()


def graphwide(x, y, xlabel="", ylabel="", title="", file=""):
    plt.figure(dpi=300, figsize=(15, 6))
    plt.scatter(x, y, marker=".")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.tight_layout()
    if file != "":
        d = os.path.dirname(file)
        f = os.path.basename(file)
        mkdirpy(d)
        plt.savefig(os.path.join(d, "wide_"+f))
        plt.close()
        #cv2.imwrite(str(file), plt)
    else:
        plt.show()
        plt.close()


def normalize(img):
    """Normalize gray img from 0 to 255 (uint8)
    Divide by 255 to get (float64)"""
    img = cv2.normalize(img, img, 0, 255, norm_type=cv2.NORM_MINMAX).astype(np.uint8)
    return img


def togray(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img


def to3channel(img):
    img = np.dstack((img, img, img))
    # img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    return img


def rssq(v):
    return np.sqrt(np.sum(v ** 2))


def rmse(v):
    return np.sqrt(mean(v ** 2))


def is_date(string, fuzzy=False):
    try:
        parsedate(string, fuzzy=fuzzy)
        return True
    except ValueError:
        return False

def interpolation(d, x):
    """d data, middle part to interpolate"""
    output = d[1][0] + (x - d[0][0]) * ((d[1][1] - d[1][0]) / (d[0][1] - d[0][0]))
    return output





def nlargestcnts3(img, n, simple=True):
    """(img, n, simple=True) Find n largest contours in binary image.
    TREE method. Pass 0 for CHAIN_APPROX_NONE.
    Deals with 0 and very small area contours
    Returns a dataframe of [area, cnt]"""
    if simple:
        approx_meth = cv2.CHAIN_APPROX_SIMPLE
    else:
        approx_meth = cv2.CHAIN_APPROX_NONE
    cnts, hiers = cv2.findContours(img, cv2.RETR_TREE, approx_meth)
    areas = np.array([])
    cntarray = []
    for j in cnts:
        a = cv2.contourArea(j)
        if len(areas) < n:
            areas = np.append(areas, a)
            cntarray.append(j)
        else:
            smlst = np.argmin(areas)
            if a > areas[smlst] or areas[smlst] == 0:
                areas = np.delete(areas, smlst)
                del cntarray[smlst]
                areas = np.append(areas, a)
                cntarray.append(j)

    bign = pd.DataFrame()
    bign["area"] = areas
    bign["cnt"] = cntarray
    return


def getlowess(x, y, f):
    return sm.nonparametric.lowess(x, y, frac=f)

def getsheetdetails(file_path):
    # https://stackoverflow.com/questions/12250024
    sheets = []
    file_name = os.path.splitext(os.path.split(file_path)[-1])[0]
    dir_name = os.path.dirname(file_path)
    # Make a temporary directory with the file name
    directory_to_extract_to = os.path.join(dir_name, file_name)
    mkdirpy(directory_to_extract_to)
    # Extract the xlsx file as it is just a zip file
    zip_ref = ZipFile(file_path, 'r')
    zip_ref.extractall(directory_to_extract_to)
    zip_ref.close()
    # Open the workbook.xml which is very light and only has meta data, get sheets from it
    path_to_workbook = os.path.join(directory_to_extract_to, 'xl', 'workbook.xml')
    with open(path_to_workbook, 'r') as f:
        xml = f.read()
        dictionary = xmltodict.parse(xml)
        if not isinstance(dictionary['workbook']['sheets']['sheet'], list):
            sheets.append(dictionary['workbook']['sheets']['sheet']['@name'])
        else:
            for sheet in dictionary['workbook']['sheets']['sheet']:
                sheets.append(sheet['@name'])
    # Delete the extracted files directory
    f.close()
    rmtree(directory_to_extract_to)
    return sheets


def getsample(samples, label):
    #if label[0] != "0":
    #    if label.find("0") > 0:
    #        label = label[:2].zfill(3) + label[2:]
    #    else:
    #        label = label[0].zfill(3) + label[1:]
    for s in samples:
        if s._label.lower() == label.lower():
            return s
    print("Could not find " + label)
    return None


def printkeys(s, br=False):
    if br:
        print("{")
        for k in sorted(s.__dict__.keys()):
            print("\t", k)
        print("}")
    else:
        print(sorted(s.__dict__.keys()))

def getkeysizes(s):  # Return size of keys if large enough to matter
    tempdir = "temp"
    mkdirpy(tempdir)
    for k, v in s.__dict__.items():
        filename = k + ".pkl"
        file = Path(tempdir) / filename
        with open(file, 'wb') as pickle_file:
            pickle.dump(v, pickle_file)
        fsize = humanize.naturalsize(os.path.getsize(file))
        if fsize[-1] == "B" and fsize[-2:] != "kB":
            print(f"{k}: {fsize}")
    rmtree(tempdir)


def getkeysizesall(s):  # Return size of keys if large enough to matter
    tempdir = "temp"
    mkdirpy(tempdir)
    for k, v in s.__dict__.items():
        filename = k + ".pkl"
        file = Path(tempdir) / filename
        with open(file, 'wb') as pickle_file:
            pickle.dump(v, pickle_file)
        fsize = humanize.naturalsize(os.path.getsize(file))
        print(f"{k}: {fsize}")
    rmtree(tempdir)


def nsdetails(s, br=False):
    print("----------------- SAMPLE METADATA ----------------")
    printkeys(s, br)
    getkeysizes(s)

def nsdetailsall(s, br=False):
    print("----------------- SAMPLE METADATA ----------------")
    printkeys(s, br)
    getkeysizesall(s)


def decimalpad(fl):
    return f"{fl:.3f}"


def comparefiles(file1, file2):
    "Do the two files have exactly the same contents?"
    # https://stackoverflow.com/a/255210
    with open(file1, "rb") as fp1, open(file2, "rb") as fp2:
        if os.fstat(fp1.fileno()).st_size != os.fstat(fp2.fileno()).st_size:
            return False  # different sizes ∴ not equal
        # set up one 4k-reader for each file
        fp1_reader = functools.partial(fp1.read, 4096)
        fp2_reader = functools.partial(fp2.read, 4096)
        # pair each 4k-chunk from the two readers while they do not return '' (EOF)
        cmp_pairs = zip(iter(fp1_reader, b''), iter(fp2_reader, b''))
        # return True for all pairs that are not equal
        inequalities = itertools.starmap(operator.ne, cmp_pairs)
        # voilà; any() stops at first True value
        return not any(inequalities)

def compareexcels(file1, file2):
    file1sheets = getsheetdetails(file1)
    file2sheets = getsheetdetails(file2)
    if file1sheets != file2sheets:
        return False
    with open(file1, "rb") as fp1, open(file2, "rb") as fp2:
        size1 = os.fstat(fp1.fileno()).st_size
        size2 = os.fstat(fp2.fileno()).st_size
        if abs(size1 - size2) > 3:
            return False  # different sizes (with some wiggle room) ∴ not equal
    fp1.close()
    fp2.close()
    df1 = load_workbook(file1, read_only=True)
    df2 = load_workbook(file2, read_only=True)
    print("Running full excel compare...")
    for sheet in file1sheets:
        sheet1 = df1[sheet]
        sheet2 = df2[sheet]
        if sheet1.calculate_dimension() != sheet2.calculate_dimension():
            return False
        sentinel = object()
        for a, b in itertools.zip_longest(sheet1.values, sheet2.values, fillvalue=sentinel):
            if a != b:
                return False
    df1.close()
    df2.close()
    return True


def writedata(path, data):
    """Dump data into pickle file in path"""
    with open(path, 'wb') as pickle_file:
        pickle.dump(data, pickle_file)
    return None


def loaddata(path):
    """Return data from pickle file in path"""
    with open(path, 'rb') as pickle_file:
        data = pickle.load(pickle_file)
    return data


def tprint(s):
    print("\t", s)




def get_largest_object(img, n=1, simple=False):
    """(img, n, simple=True) Find n largest contours in binary image.
    TREE method. Pass 0 for CHAIN_APPROX_NONE.
    Deals with 0 and very small area contours
    Returns a dataframe of [area, cnt]"""
    if simple:
        approx_meth = cv2.CHAIN_APPROX_SIMPLE
    else:
        approx_meth = cv2.CHAIN_APPROX_NONE
    cnts, hiers = cv2.findContours(img, cv2.RETR_TREE, approx_meth)
    areas = np.array([])
    cntarray = []
    for j in cnts:
        a = cv2.contourArea(j)
        if len(areas) < n:
            areas = np.append(areas, a)
            cntarray.append(j)
        else:
            smlst = np.argmin(areas)
            if a > areas[smlst] or areas[smlst] == 0:
                areas = np.delete(areas, smlst)
                del cntarray[smlst]
                areas = np.append(areas, a)
                cntarray.append(j)
    cnt = cntarray[0]
    canv = cv2.drawContours(np.zeros(img.shape), [cnt], -1, 1, -1)
    return canv


def make_video(filepath, data, fps):
    """ filepath - where the video will be saved
        data - list of images to make into video
        fps - frames per second"""
    if len(data[0].shape) == 3:
        size = data[0].shape[::-1][1:3]
        is_color = True
    else:
        size = data[0].shape[::-1]
        is_color = False
    print(size)
    video = cv2.VideoWriter(str(filepath),
                            cv2.VideoWriter_fourcc(*"mp4v"),  # May need to try "xvid" or "divx"
                            fps, size, is_color)
    for img in data:
        video.write(img)
    cv2.destroyAllWindows()
    video.release()


def img_cleanup(img):
    kernel = np.ones((5, 5), np.uint8)
    opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    canv = get_largest_object(opening)
    return canv.astype(np.uint8)