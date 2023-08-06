define(["@jupyter-widgets/base"], function(__WEBPACK_EXTERNAL_MODULE_1__) { return /******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, {
/******/ 				configurable: false,
/******/ 				enumerable: true,
/******/ 				get: getter
/******/ 			});
/******/ 		}
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = 6);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
var __extends = (this && this.__extends) || (function () {
    var extendStatics = Object.setPrototypeOf ||
        ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
        function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
var __assign = (this && this.__assign) || Object.assign || function(t) {
    for (var s, i = 1, n = arguments.length; i < n; i++) {
        s = arguments[i];
        for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
            t[p] = s[p];
    }
    return t;
};
Object.defineProperty(exports, "__esModule", { value: true });
var base_1 = __webpack_require__(7);
var ndarray = __webpack_require__(3);
;
function JSONToArray(obj, manager) {
    if (obj === null) {
        return null;
    }
    // obj is {shape: list, dtype: string, array: DataView}
    // return an ndarray object
    return ndarray(new exports.typesToArray[obj.dtype](obj.buffer.buffer), obj.shape);
}
exports.JSONToArray = JSONToArray;
function arrayToJSON(obj, widget) {
    if (obj === null) {
        return null;
    }
    // serialize to {shape: list, dtype: string, array: buffer}
    return { shape: obj.shape, dtype: obj.dtype, buffer: obj.data };
}
exports.arrayToJSON = arrayToJSON;
exports.array_serialization = { deserialize: JSONToArray, serialize: arrayToJSON };
exports.typesToArray = {
    int8: Int8Array,
    int16: Int16Array,
    int32: Int32Array,
    uint8: Uint8Array,
    uint16: Uint16Array,
    uint32: Uint32Array,
    float32: Float32Array,
    float64: Float64Array
};
var NDArrayModel = (function (_super) {
    __extends(NDArrayModel, _super);
    function NDArrayModel() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    NDArrayModel.prototype.defaults = function () {
        return __assign({}, _super.prototype.defaults.call(this), {
            array: ndarray([]),
            _model_name: NDArrayModel.model_name,
        });
    };
    NDArrayModel.serializers = __assign({}, base_1.DataModel.serializers, { array: exports.array_serialization });
    NDArrayModel.model_name = 'NDArrayModel';
    return NDArrayModel;
}(base_1.DataModel));
exports.NDArrayModel = NDArrayModel;


/***/ }),
/* 1 */
/***/ (function(module, exports) {

module.exports = __WEBPACK_EXTERNAL_MODULE_1__;

/***/ }),
/* 2 */
/***/ (function(module, exports) {

module.exports = {"name":"jupyter-datawidgets","version":"2.1.0","description":"A set of widgets to help facilitate reuse of large datasets across widgets","main":"lib/index.js","types":"./lib/index.d.ts","scripts":{"clean:lib":"rimraf lib","clean:nbextension":"rimraf ../../ipydatawidgets/nbextension/static/index.js","clean":"npm run clean:lib && npm run clean:nbextension","build:nbextension":"webpack","build:lib":"tsc --project src","build":"npm run build:lib && npm run build:nbextension","test":"npm run test:firefox","test:chrome":"karma start --browsers=Chrome tests/karma.conf.js","test:debug":"karma start --browsers=Chrome --singleRun=false --debug=true tests/karma.conf.js","test:firefox":"karma start --browsers=Firefox tests/karma.conf.js","test:ie":"karma start --browsers=IE tests/karma.conf.js","prepublish":"npm run clean && npm run build"},"keywords":["jupyter","widgets"],"author":"Vidar T. Fauske","license":"BSD-3-Clause","devDependencies":{"@types/expect.js":"^0.3.29","@types/mocha":"^2.2.41","@types/node":"^8.0.17","expect.js":"^0.3.1","json-loader":"^0.5.7","karma":"^1.7.0","karma-chrome-launcher":"^2.2.0","karma-firefox-launcher":"^1.0.1","karma-ie-launcher":"^1.0.0","karma-mocha":"^1.3.0","karma-mocha-reporter":"^2.2.3","karma-typescript":"^3.0.5","mocha":"^3.5.0","source-map-loader":"^0.2.1","ts-loader":"^2.3.2","typescript":"~2.4.2","webpack":"^3.4.1"},"dependencies":{"@jupyter-widgets/base":"^1.0.1","jupyter-scales":"^1.0.1","ndarray":"^1.0.18"}}

/***/ }),
/* 3 */
/***/ (function(module, exports, __webpack_require__) {

var iota = __webpack_require__(8)
var isBuffer = __webpack_require__(9)

var hasTypedArrays  = ((typeof Float64Array) !== "undefined")

function compare1st(a, b) {
  return a[0] - b[0]
}

function order() {
  var stride = this.stride
  var terms = new Array(stride.length)
  var i
  for(i=0; i<terms.length; ++i) {
    terms[i] = [Math.abs(stride[i]), i]
  }
  terms.sort(compare1st)
  var result = new Array(terms.length)
  for(i=0; i<result.length; ++i) {
    result[i] = terms[i][1]
  }
  return result
}

function compileConstructor(dtype, dimension) {
  var className = ["View", dimension, "d", dtype].join("")
  if(dimension < 0) {
    className = "View_Nil" + dtype
  }
  var useGetters = (dtype === "generic")

  if(dimension === -1) {
    //Special case for trivial arrays
    var code =
      "function "+className+"(a){this.data=a;};\
var proto="+className+".prototype;\
proto.dtype='"+dtype+"';\
proto.index=function(){return -1};\
proto.size=0;\
proto.dimension=-1;\
proto.shape=proto.stride=proto.order=[];\
proto.lo=proto.hi=proto.transpose=proto.step=\
function(){return new "+className+"(this.data);};\
proto.get=proto.set=function(){};\
proto.pick=function(){return null};\
return function construct_"+className+"(a){return new "+className+"(a);}"
    var procedure = new Function(code)
    return procedure()
  } else if(dimension === 0) {
    //Special case for 0d arrays
    var code =
      "function "+className+"(a,d) {\
this.data = a;\
this.offset = d\
};\
var proto="+className+".prototype;\
proto.dtype='"+dtype+"';\
proto.index=function(){return this.offset};\
proto.dimension=0;\
proto.size=1;\
proto.shape=\
proto.stride=\
proto.order=[];\
proto.lo=\
proto.hi=\
proto.transpose=\
proto.step=function "+className+"_copy() {\
return new "+className+"(this.data,this.offset)\
};\
proto.pick=function "+className+"_pick(){\
return TrivialArray(this.data);\
};\
proto.valueOf=proto.get=function "+className+"_get(){\
return "+(useGetters ? "this.data.get(this.offset)" : "this.data[this.offset]")+
"};\
proto.set=function "+className+"_set(v){\
return "+(useGetters ? "this.data.set(this.offset,v)" : "this.data[this.offset]=v")+"\
};\
return function construct_"+className+"(a,b,c,d){return new "+className+"(a,d)}"
    var procedure = new Function("TrivialArray", code)
    return procedure(CACHED_CONSTRUCTORS[dtype][0])
  }

  var code = ["'use strict'"]

  //Create constructor for view
  var indices = iota(dimension)
  var args = indices.map(function(i) { return "i"+i })
  var index_str = "this.offset+" + indices.map(function(i) {
        return "this.stride[" + i + "]*i" + i
      }).join("+")
  var shapeArg = indices.map(function(i) {
      return "b"+i
    }).join(",")
  var strideArg = indices.map(function(i) {
      return "c"+i
    }).join(",")
  code.push(
    "function "+className+"(a," + shapeArg + "," + strideArg + ",d){this.data=a",
      "this.shape=[" + shapeArg + "]",
      "this.stride=[" + strideArg + "]",
      "this.offset=d|0}",
    "var proto="+className+".prototype",
    "proto.dtype='"+dtype+"'",
    "proto.dimension="+dimension)

  //view.size:
  code.push("Object.defineProperty(proto,'size',{get:function "+className+"_size(){\
return "+indices.map(function(i) { return "this.shape["+i+"]" }).join("*"),
"}})")

  //view.order:
  if(dimension === 1) {
    code.push("proto.order=[0]")
  } else {
    code.push("Object.defineProperty(proto,'order',{get:")
    if(dimension < 4) {
      code.push("function "+className+"_order(){")
      if(dimension === 2) {
        code.push("return (Math.abs(this.stride[0])>Math.abs(this.stride[1]))?[1,0]:[0,1]}})")
      } else if(dimension === 3) {
        code.push(
"var s0=Math.abs(this.stride[0]),s1=Math.abs(this.stride[1]),s2=Math.abs(this.stride[2]);\
if(s0>s1){\
if(s1>s2){\
return [2,1,0];\
}else if(s0>s2){\
return [1,2,0];\
}else{\
return [1,0,2];\
}\
}else if(s0>s2){\
return [2,0,1];\
}else if(s2>s1){\
return [0,1,2];\
}else{\
return [0,2,1];\
}}})")
      }
    } else {
      code.push("ORDER})")
    }
  }

  //view.set(i0, ..., v):
  code.push(
"proto.set=function "+className+"_set("+args.join(",")+",v){")
  if(useGetters) {
    code.push("return this.data.set("+index_str+",v)}")
  } else {
    code.push("return this.data["+index_str+"]=v}")
  }

  //view.get(i0, ...):
  code.push("proto.get=function "+className+"_get("+args.join(",")+"){")
  if(useGetters) {
    code.push("return this.data.get("+index_str+")}")
  } else {
    code.push("return this.data["+index_str+"]}")
  }

  //view.index:
  code.push(
    "proto.index=function "+className+"_index(", args.join(), "){return "+index_str+"}")

  //view.hi():
  code.push("proto.hi=function "+className+"_hi("+args.join(",")+"){return new "+className+"(this.data,"+
    indices.map(function(i) {
      return ["(typeof i",i,"!=='number'||i",i,"<0)?this.shape[", i, "]:i", i,"|0"].join("")
    }).join(",")+","+
    indices.map(function(i) {
      return "this.stride["+i + "]"
    }).join(",")+",this.offset)}")

  //view.lo():
  var a_vars = indices.map(function(i) { return "a"+i+"=this.shape["+i+"]" })
  var c_vars = indices.map(function(i) { return "c"+i+"=this.stride["+i+"]" })
  code.push("proto.lo=function "+className+"_lo("+args.join(",")+"){var b=this.offset,d=0,"+a_vars.join(",")+","+c_vars.join(","))
  for(var i=0; i<dimension; ++i) {
    code.push(
"if(typeof i"+i+"==='number'&&i"+i+">=0){\
d=i"+i+"|0;\
b+=c"+i+"*d;\
a"+i+"-=d}")
  }
  code.push("return new "+className+"(this.data,"+
    indices.map(function(i) {
      return "a"+i
    }).join(",")+","+
    indices.map(function(i) {
      return "c"+i
    }).join(",")+",b)}")

  //view.step():
  code.push("proto.step=function "+className+"_step("+args.join(",")+"){var "+
    indices.map(function(i) {
      return "a"+i+"=this.shape["+i+"]"
    }).join(",")+","+
    indices.map(function(i) {
      return "b"+i+"=this.stride["+i+"]"
    }).join(",")+",c=this.offset,d=0,ceil=Math.ceil")
  for(var i=0; i<dimension; ++i) {
    code.push(
"if(typeof i"+i+"==='number'){\
d=i"+i+"|0;\
if(d<0){\
c+=b"+i+"*(a"+i+"-1);\
a"+i+"=ceil(-a"+i+"/d)\
}else{\
a"+i+"=ceil(a"+i+"/d)\
}\
b"+i+"*=d\
}")
  }
  code.push("return new "+className+"(this.data,"+
    indices.map(function(i) {
      return "a" + i
    }).join(",")+","+
    indices.map(function(i) {
      return "b" + i
    }).join(",")+",c)}")

  //view.transpose():
  var tShape = new Array(dimension)
  var tStride = new Array(dimension)
  for(var i=0; i<dimension; ++i) {
    tShape[i] = "a[i"+i+"]"
    tStride[i] = "b[i"+i+"]"
  }
  code.push("proto.transpose=function "+className+"_transpose("+args+"){"+
    args.map(function(n,idx) { return n + "=(" + n + "===undefined?" + idx + ":" + n + "|0)"}).join(";"),
    "var a=this.shape,b=this.stride;return new "+className+"(this.data,"+tShape.join(",")+","+tStride.join(",")+",this.offset)}")

  //view.pick():
  code.push("proto.pick=function "+className+"_pick("+args+"){var a=[],b=[],c=this.offset")
  for(var i=0; i<dimension; ++i) {
    code.push("if(typeof i"+i+"==='number'&&i"+i+">=0){c=(c+this.stride["+i+"]*i"+i+")|0}else{a.push(this.shape["+i+"]);b.push(this.stride["+i+"])}")
  }
  code.push("var ctor=CTOR_LIST[a.length+1];return ctor(this.data,a,b,c)}")

  //Add return statement
  code.push("return function construct_"+className+"(data,shape,stride,offset){return new "+className+"(data,"+
    indices.map(function(i) {
      return "shape["+i+"]"
    }).join(",")+","+
    indices.map(function(i) {
      return "stride["+i+"]"
    }).join(",")+",offset)}")

  //Compile procedure
  var procedure = new Function("CTOR_LIST", "ORDER", code.join("\n"))
  return procedure(CACHED_CONSTRUCTORS[dtype], order)
}

function arrayDType(data) {
  if(isBuffer(data)) {
    return "buffer"
  }
  if(hasTypedArrays) {
    switch(Object.prototype.toString.call(data)) {
      case "[object Float64Array]":
        return "float64"
      case "[object Float32Array]":
        return "float32"
      case "[object Int8Array]":
        return "int8"
      case "[object Int16Array]":
        return "int16"
      case "[object Int32Array]":
        return "int32"
      case "[object Uint8Array]":
        return "uint8"
      case "[object Uint16Array]":
        return "uint16"
      case "[object Uint32Array]":
        return "uint32"
      case "[object Uint8ClampedArray]":
        return "uint8_clamped"
    }
  }
  if(Array.isArray(data)) {
    return "array"
  }
  return "generic"
}

var CACHED_CONSTRUCTORS = {
  "float32":[],
  "float64":[],
  "int8":[],
  "int16":[],
  "int32":[],
  "uint8":[],
  "uint16":[],
  "uint32":[],
  "array":[],
  "uint8_clamped":[],
  "buffer":[],
  "generic":[]
}

;(function() {
  for(var id in CACHED_CONSTRUCTORS) {
    CACHED_CONSTRUCTORS[id].push(compileConstructor(id, -1))
  }
});

function wrappedNDArrayCtor(data, shape, stride, offset) {
  if(data === undefined) {
    var ctor = CACHED_CONSTRUCTORS.array[0]
    return ctor([])
  } else if(typeof data === "number") {
    data = [data]
  }
  if(shape === undefined) {
    shape = [ data.length ]
  }
  var d = shape.length
  if(stride === undefined) {
    stride = new Array(d)
    for(var i=d-1, sz=1; i>=0; --i) {
      stride[i] = sz
      sz *= shape[i]
    }
  }
  if(offset === undefined) {
    offset = 0
    for(var i=0; i<d; ++i) {
      if(stride[i] < 0) {
        offset -= (shape[i]-1)*stride[i]
      }
    }
  }
  var dtype = arrayDType(data)
  var ctor_list = CACHED_CONSTRUCTORS[dtype]
  while(ctor_list.length <= d+1) {
    ctor_list.push(compileConstructor(dtype, ctor_list.length-1))
  }
  var ctor = ctor_list[d+1]
  return ctor(data, shape, stride, offset)
}

module.exports = wrappedNDArrayCtor


/***/ }),
/* 4 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
Object.defineProperty(exports, "__esModule", { value: true });
var base_1 = __webpack_require__(1);
var ndarray_1 = __webpack_require__(0);
/**
 * Deserializes union JSON to an ndarray or a NDArrayModel, as appropriate.
 */
function JSONToUnion(obj, manager) {
    if (typeof obj === 'string') {
        var modelPromise = base_1.unpack_models(obj, manager);
        return modelPromise;
    }
    else {
        return Promise.resolve(ndarray_1.JSONToArray(obj, manager));
    }
}
exports.JSONToUnion = JSONToUnion;
/**
 * Deserializes union JSON to an ndarray, regardless of whether it is a widget reference or direct data.
 */
function JSONToUnionArray(obj, manager) {
    if (typeof obj === 'string') {
        var modelPromise = base_1.unpack_models(obj, manager);
        return modelPromise.then(function (model) {
            return model.get('array');
        });
    }
    else {
        return Promise.resolve(ndarray_1.JSONToArray(obj, manager));
    }
}
exports.JSONToUnionArray = JSONToUnionArray;
/**
 * Serializes a union to JSON.
 */
function unionToJSON(obj, widget) {
    if (obj instanceof ndarray_1.NDArrayModel) {
        return obj.toJSON(undefined);
    }
    else {
        return ndarray_1.arrayToJSON(obj, widget);
    }
}
exports.unionToJSON = unionToJSON;
/**
 * Gets the array of a union.
 */
function getArrayFromUnion(union) {
    if (union instanceof ndarray_1.NDArrayModel) {
        return union.get('array');
    }
    return union;
}
exports.getArrayFromUnion = getArrayFromUnion;
/**
 * Sets up backbone events for listening to union changes.
 *
 * The callback will be called when:
 *  - The model is a widget, and its data changes
 *
 * Specify `allChanges` as truthy to also cover these cases:
 *  - The union changes from a widget to an array or vice-versa
 *  - The union is an array and its content changes
 *
 * To stop listening, call the return value.
 */
function listenToUnion(model, unionName, callback, allChanges) {
    function listenToWidgetChanges(union) {
        if (union instanceof ndarray_1.NDArrayModel) {
            // listen to changes in current model
            model.listenTo(union, 'change', callback);
        }
    }
    function onUnionChange(unionModel, value, subOptions) {
        var prev = model.previous(unionName) || [];
        var curr = value || [];
        if (prev instanceof ndarray_1.NDArrayModel) {
            model.stopListening(prev);
        }
        else if (allChanges && !(curr instanceof ndarray_1.NDArrayModel)) {
            // The union was an array, and has changed to a new array
            callback(unionModel, subOptions);
        }
        if (allChanges && (prev instanceof ndarray_1.NDArrayModel) !== (curr instanceof ndarray_1.NDArrayModel)) {
            // Union type has changed, call out
            callback(unionModel, subOptions);
        }
        listenToWidgetChanges(curr);
    }
    listenToWidgetChanges(model.get(unionName));
    // make sure to (un)hook listeners when property changes
    model.on('change:' + unionName, onUnionChange);
    function stopListening() {
        var curr = model.get(unionName);
        if (curr instanceof ndarray_1.NDArrayModel) {
            model.stopListening(curr);
        }
        model.off('change:' + unionName, onUnionChange);
    }
    return stopListening;
}
exports.listenToUnion = listenToUnion;
exports.data_union_array_serialization = { deserialize: JSONToUnionArray, serialize: unionToJSON };
exports.data_union_serialization = { deserialize: JSONToUnion, serialize: unionToJSON };


/***/ }),
/* 5 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
var __extends = (this && this.__extends) || (function () {
    var extendStatics = Object.setPrototypeOf ||
        ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
        function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
var __assign = (this && this.__assign) || Object.assign || function(t) {
    for (var s, i = 1, n = arguments.length; i < n; i++) {
        s = arguments[i];
        for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
            t[p] = s[p];
    }
    return t;
};
Object.defineProperty(exports, "__esModule", { value: true });
var base_1 = __webpack_require__(1);
var ndarray_1 = __webpack_require__(0);
var union_1 = __webpack_require__(4);
var ndarray = __webpack_require__(3);
/**
 * Utility to create a copy of an ndarray
 *
 * @param {ndarray.NDArray} array
 * @returns {ndarray.NDArray}
 */
function copyArray(array, dtype) {
    if (dtype === undefined) {
        return ndarray(array.data.slice(), array.shape, array.stride, array.offset);
    }
    return ndarray(new ndarray_1.typesToArray[dtype](array.data), array.shape, array.stride, array.offset);
}
exports.copyArray = copyArray;
/**
 * Scaled array model.
 *
 * This model provides a scaled version of an array, that is
 * automatically recomputed when either the array or the scale
 * changes.
 *
 * It triggers an event 'change:scaledData' when the array is
 * recomputed. Note: 'scaledData' is a direct propetry, not a
 * model attribute. The event triggers with an argument
 * { resized: boolean}, which indicates whether the array changed
 * size. Note: When the 'resized' flag is false, the old array will
 * have been reused, otherwise a new array is allocated.
 *
 * @export
 * @class ScaledArrayModel
 * @extends {DataModel}
 */
var ScaledArrayModel = (function (_super) {
    __extends(ScaledArrayModel, _super);
    function ScaledArrayModel() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        /**
         * The scaled data array.
         *
         * @type {(ndarray.NDArray | null)}
         * @memberof ScaledArrayModel
         */
        _this.scaledData = null;
        return _this;
    }
    ScaledArrayModel.prototype.defaults = function () {
        return __assign({}, _super.prototype.defaults.call(this), {
            array: ndarray([]),
            scale: null,
            _model_name: ScaledArrayModel.model_name,
        });
    };
    /**
     * (Re-)compute the scaledData data.
     *
     * @returns {void}
     * @memberof ScaledArrayModel
     */
    ScaledArrayModel.prototype.computeScaledData = function () {
        var array = union_1.getArrayFromUnion(this.get('array'));
        var scale = this.get('scale');
        // Handle null case immediately:
        if (array === null || scale === null) {
            var changed = this.scaledData !== null;
            this.scaledData = null;
            if (changed) {
                this.trigger('change:scaledData', { resized: true });
            }
            return;
        }
        var resized = this.arrayMismatch();
        if (resized) {
            // Allocate new array
            this.scaledData = copyArray(array, this.scaledDtype());
        }
        var data = array.data;
        var target = this.scaledData.data;
        // Set values:
        for (var i = 0; i < data.length; ++i) {
            target[i] = scale.obj(data[i]);
        }
        this.trigger('change:scaledData', { resized: resized });
    };
    /**
     * Initialize the model
     *
     * @param {Backbone.ObjectHash} attributes
     * @param {{model_id: string; comm?: any; widget_manager: any; }} options
     * @memberof ScaledArrayModel
     */
    ScaledArrayModel.prototype.initialize = function (attributes, options) {
        var _this = this;
        _super.prototype.initialize.call(this, attributes, options);
        this.initPromise = Promise.resolve().then(function () {
            _this.computeScaledData();
            _this.setupListeners();
        });
    };
    /**
     * Sets up any relevant event listeners after the object has been initialized,
     * but before the initPromise is resolved.
     *
     * @memberof ScaledArrayModel
     */
    ScaledArrayModel.prototype.setupListeners = function () {
        // Listen to direct changes on our model:
        this.on('change', this.onChange, this);
        // Listen to changes within array and scale models:
        union_1.listenToUnion(this, 'array', this.onChange.bind(this));
        this.listenTo(this.get('scale'), 'change', this.onChange);
    };
    /**
     * Callback for when the source data changes.
     *
     * @param {WidgetModel} model
     * @memberof ScaledArrayModel
     */
    ScaledArrayModel.prototype.onChange = function (model) {
        this.computeScaledData();
    };
    /**
     * Whether the array and scaledData have a mismatch in shape or type.
     *
     * @protected
     * @returns {boolean}
     * @memberof ScaledArrayModel
     */
    ScaledArrayModel.prototype.arrayMismatch = function () {
        var array = union_1.getArrayFromUnion(this.get('array'));
        if (array === null && this.scaledData === null) {
            return false;
        }
        return array === null || this.scaledData === null ||
            JSON.stringify(array.shape) !== JSON.stringify(this.scaledData.shape) ||
            array.dtype !== this.scaledData.dtype;
    };
    ScaledArrayModel.prototype.scaledDtype = function () {
        var array = union_1.getArrayFromUnion(this.get('array'));
        if (array === null) {
            return undefined;
        }
        return array.dtype;
    };
    ScaledArrayModel.serializers = __assign({}, ndarray_1.NDArrayModel.serializers, { array: union_1.data_union_serialization, scale: { deserialize: base_1.unpack_models } });
    ScaledArrayModel.model_name = 'ScaledArrayModel';
    return ScaledArrayModel;
}(ndarray_1.NDArrayModel));
exports.ScaledArrayModel = ScaledArrayModel;


/***/ }),
/* 6 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

Object.defineProperty(exports, "__esModule", { value: true });
var ndarray_1 = __webpack_require__(0);
exports.NDArrayModel = ndarray_1.NDArrayModel;
exports.JSONToArray = ndarray_1.JSONToArray;
exports.arrayToJSON = ndarray_1.arrayToJSON;
exports.array_serialization = ndarray_1.array_serialization;
var union_1 = __webpack_require__(4);
exports.JSONToUnion = union_1.JSONToUnion;
exports.JSONToUnionArray = union_1.JSONToUnionArray;
exports.unionToJSON = union_1.unionToJSON;
exports.data_union_serialization = union_1.data_union_serialization;
exports.data_union_array_serialization = union_1.data_union_array_serialization;
exports.getArrayFromUnion = union_1.getArrayFromUnion;
exports.listenToUnion = union_1.listenToUnion;
var scaled_1 = __webpack_require__(5);
exports.ScaledArrayModel = scaled_1.ScaledArrayModel;
var common_1 = __webpack_require__(10);
exports.getArray = common_1.getArray;
var version_1 = __webpack_require__(11);
exports.JUPYTER_DATAWIDGETS_VERSION = version_1.JUPYTER_DATAWIDGETS_VERSION;
exports.version = __webpack_require__(2).version;


/***/ }),
/* 7 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
var __extends = (this && this.__extends) || (function () {
    var extendStatics = Object.setPrototypeOf ||
        ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
        function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
var __assign = (this && this.__assign) || Object.assign || function(t) {
    for (var s, i = 1, n = arguments.length; i < n; i++) {
        s = arguments[i];
        for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
            t[p] = s[p];
    }
    return t;
};
Object.defineProperty(exports, "__esModule", { value: true });
var base_1 = __webpack_require__(1);
exports.version = __webpack_require__(2).version;
var DataModel = (function (_super) {
    __extends(DataModel, _super);
    function DataModel() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    DataModel.prototype.defaults = function () {
        return __assign({}, _super.prototype.defaults.call(this), {
            _model_module: DataModel.model_module,
            _model_module_version: DataModel.model_module_version,
            _view_name: DataModel.view_name,
            _view_module: DataModel.view_module,
            _view_module_version: DataModel.view_module_version,
        });
    };
    DataModel.serializers = __assign({}, base_1.WidgetModel.serializers);
    DataModel.model_module = 'jupyter-datawidgets';
    DataModel.model_module_version = exports.version;
    DataModel.view_name = null;
    DataModel.view_module = null;
    DataModel.view_module_version = '';
    return DataModel;
}(base_1.WidgetModel));
exports.DataModel = DataModel;


/***/ }),
/* 8 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


function iota(n) {
  var result = new Array(n)
  for(var i=0; i<n; ++i) {
    result[i] = i
  }
  return result
}

module.exports = iota

/***/ }),
/* 9 */
/***/ (function(module, exports) {

/*!
 * Determine if an object is a Buffer
 *
 * @author   Feross Aboukhadijeh <feross@feross.org> <http://feross.org>
 * @license  MIT
 */

// The _isBuffer check is for Safari 5-7 support, because it's missing
// Object.prototype.constructor. Remove this eventually
module.exports = function (obj) {
  return obj != null && (isBuffer(obj) || isSlowBuffer(obj) || !!obj._isBuffer)
}

function isBuffer (obj) {
  return !!obj.constructor && typeof obj.constructor.isBuffer === 'function' && obj.constructor.isBuffer(obj)
}

// For Node v0.10 support. Remove this eventually.
function isSlowBuffer (obj) {
  return typeof obj.readFloatLE === 'function' && typeof obj.slice === 'function' && isBuffer(obj.slice(0, 0))
}


/***/ }),
/* 10 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

Object.defineProperty(exports, "__esModule", { value: true });
var ndarray_1 = __webpack_require__(0);
var scaled_1 = __webpack_require__(5);
/**
 * Gets the array of any array source.
 */
function getArray(data) {
    if (data instanceof ndarray_1.NDArrayModel) {
        if (data instanceof scaled_1.ScaledArrayModel) {
            return data.scaledData;
        }
        return data.get('array');
    }
    return data;
}
exports.getArray = getArray;


/***/ }),
/* 11 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
Object.defineProperty(exports, "__esModule", { value: true });
/**
 * The version of the Jupyter data widgets attribute spec that this package
 * implements.
 */
exports.JUPYTER_DATAWIDGETS_VERSION = '1.0.0';


/***/ })
/******/ ])});;
//# sourceMappingURL=index.js.map