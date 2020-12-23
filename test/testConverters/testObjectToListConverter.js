const expect = require("chai").expect;
const objectToListConverter = require("../../converters/objectToListConverter");

let objListType1 = {
    one: {
        two: 3,
        four: [5, 6, 7],
    },
    eight: {
        nine: {
            ten: 11,
        },
    },
}

describe("Test objectToListConverter", function () {
    it("converts object to list of objListType1", function () {
        const list = objectToListConverter(objListType1);
        expect(list).to.eql({
                'one/two': 3,
                'one/four/0': 5,
                'one/four/1': 6,
                'one/four/2': 7,
                'eight/nine/ten': 11
            }
        )
    })
})

let objListType2 = {
    one: {
        two: 3,
        four: {
            five: {
                six: {
                    seven: [8]
                }
            }
        }
    },
    eight: 11
}

describe("Test listToObjectConverter", function () {
    it("converts list to object of objListType2", function () {
        const list = objectToListConverter(objListType2);

        expect(list).to.eql({
                'one/two': 3,
                'one/four/five/six/seven/0': 8,
                'eight': 11
            }
        )
    })
})

describe("Test objectToListConverter", function () {
    it("converts object to list with empty object", function () {
        const list = objectToListConverter({});

        expect(list).to.eql({});
    })
})

describe("Test objectToListConverter", function () {
    it("converts object to list with object parameter as null", function () {
        const list = objectToListConverter(null);

        expect(list).to.eql({});
    })
})
