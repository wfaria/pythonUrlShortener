class BaseConverter:
    """
    This class is used to convert numbers to a specific base and vice-versa.
    The base is defined by the number of symbols characters and
    the values by each character index on the string.
    
    For example, if you use the string "abcdef", it will convert the input number to a 
    "base six encoding". So "0" will become "a", "1" will become "b", 
    "8" will become "bc" since it is (1 * 6^1) + (2 * 6^0) and etc.
    """
    
    def __init__(self, symbols):
        self.symbols = symbols;
        self.baseSize = len(symbols);
        
    def encode(self, number):
        """
        Transforms the integer number into an encoded number based
        on the symbols string.
        """
        if (type(number) != int):
            raise TypeError("Parameter with wrong type, expected int, got {0}".format(type(number)));
    
        if (number == 0):
            return "" + self.symbols[0];
           
        if (number < 0):
            sign = -1;
            number = number * sign;
        else:
            sign = 1;
        
        digits = [];
        while (number > 0):
            baseDigit = self.symbols[ int(number % self.baseSize) ];
            digits.append(baseDigit);
            number = number / self.baseSize;
            
        if (sign < 0):
            digits.append("-");
        
        digits.reverse();
        return "".join(digits);         

        
    def decode(self, baseNumber):
        """
        Transforms the string baseNumber into a normal decimal number.
        The parameter string should contain only characters which are part of the
        symbols set, otherwise this method will fail.
        """
        if (type(baseNumber) != str and type(baseNumber) != unicode):
            raise TypeError("Parameter with wrong type, expected string or unicode, got {0}".format(type(baseNumber)));
            
        sign = 1;
        if (baseNumber[0] == '-'):
            sign = -1;
            baseNumber = baseNumber[1:];
            
        num = 0;
        aux = 1;
        
        # Loop with negative step from len(baseNumber)-1 until 0.
        for i in range(len(baseNumber) - 1, -1, -1):
            currentDigit = self.symbols.find(baseNumber[i]);
            if (currentDigit == -1):
                raise ValueError("{0} isn't part of the base symbols".format(baseNumber[i]));
                
            num = num + aux * currentDigit;
            aux = aux * self.baseSize;
            
        return sign * num;

def debugPrintEncode(converter, number, expectedValue):
    encodedNumber = converter.encode(number);
    print("Number Input: {0}, output: {1}, expected encode: {2}".format(number, encodedNumber, expectedValue));
    debugPrintDecode(converter, encodedNumber, number);
    
def debugPrintDecode(converter, baseNumber, expectedValue):
    print("Encoded Input: {0}, output: {1}, expected decode: {2}".format(baseNumber, converter.decode(baseNumber), expectedValue));
        
if __name__ == "__main__":
    symbols = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
    converter = BaseConverter(symbols);
    debugPrintEncode(converter, 0, "0");
    debugPrintEncode(converter, len(symbols) - 1, "Z");
    debugPrintEncode(converter, len(symbols), "10");
    debugPrintEncode(converter, -(2*len(symbols) + 3), "-23");
    debugPrintEncode(converter, len(symbols)**4 + 36 * len(symbols)**2 + 10, "10A0a");
    debugPrintEncode(converter, len(symbols)**8 - 2, "ZZZZZZY");
        