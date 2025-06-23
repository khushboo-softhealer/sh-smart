! function (e, t) {
    "object" == typeof exports && "object" == typeof module ? module.exports = t() : "function" == typeof define && define
      .amd ? define("Supervisor", [], t) : "object" == typeof exports ? exports.Supervisor = t() : e.Supervisor = t()
  }("undefined" != typeof self ? self : this, (() => (() => {
    "use strict";
    var e = {
        8088: (e, t, r) => {
          r.d(t, {
            Z: () => p
          });
          var i = r(9601),
            n = r.n(i),
            o = r(2609),
            a = r.n(o),
            s = r(8991),
            c = r.n(s),
            l = new URL(r(8632), r.b),
            d = a()(n()),
            u = c()(l);
          d.push([e.id,
            ".KFMEJtkQQh6VP60xdodM{background-color:var(--background-color);border-radius:3px;box-shadow:0 0 3px 0 rgba(0,0,0,.5);display:flex;flex:auto;flex-direction:column;left:0;overflow:hidden;position:fixed;top:0;visibility:visible;z-index:1}.KFMEJtkQQh6VP60xdodM>.MaG6OfsVlubNNO4TeoRQ{align-items:center;background:var(--primary-color);display:flex;font-weight:700;padding:10px 15px;white-space:nowrap}.KFMEJtkQQh6VP60xdodM>.MaG6OfsVlubNNO4TeoRQ>.pNQCYApFqkn5N4pvFmYn{color:var(--background-color);cursor:default;flex:1}.KFMEJtkQQh6VP60xdodM>.MaG6OfsVlubNNO4TeoRQ>.wnN5ha1YAuW5AiVg6NGX{background:50%/50% var(--background-color) url(" +
            u +
            ") no-repeat;border-radius:50%;cursor:pointer;height:20px;min-height:20px;min-width:20px;opacity:1;width:20px}.KFMEJtkQQh6VP60xdodM>.MaG6OfsVlubNNO4TeoRQ>.wnN5ha1YAuW5AiVg6NGX:hover{opacity:.8}.KFMEJtkQQh6VP60xdodM>.b4KTZE9QYRS3GBc4f8oH{display:table;flex:1}.KFMEJtkQQh6VP60xdodM>.b4KTZE9QYRS3GBc4f8oH input.tMJ6stmo6_eewwnrQYtg{background:inherit;border:none;padding:0;text-align:end}.KFMEJtkQQh6VP60xdodM>.b4KTZE9QYRS3GBc4f8oH>.I2iV3n5EHDtHhDyLhiqP{background-color:var(--secondary-color);border:1px solid var(--foreground-color);box-sizing:border-box;color:var(--foreground-color);cursor:text;display:block;font-size:1.2em;margin:2px;padding:10px;text-align:right;width:250px}.KFMEJtkQQh6VP60xdodM>.b4KTZE9QYRS3GBc4f8oH>.I2iV3n5EHDtHhDyLhiqP>.tMJ6stmo6_eewwnrQYtg{display:block;width:225px}.KFMEJtkQQh6VP60xdodM>.b4KTZE9QYRS3GBc4f8oH>.qyFAAcsJGzEmmG4p73Lm{display:block;margin:2px}.KFMEJtkQQh6VP60xdodM>.b4KTZE9QYRS3GBc4f8oH>.qyFAAcsJGzEmmG4p73Lm>.MGe5iZTkFHemhqzswxPK{display:block}.KFMEJtkQQh6VP60xdodM>.b4KTZE9QYRS3GBc4f8oH .a9nFpIr7oIn7BaeaRJNH{cursor:pointer;display:table-cell;font-size:16px;height:30px;margin:1px;text-align:center;-webkit-user-select:none;-moz-user-select:none;user-select:none;vertical-align:middle}.KFMEJtkQQh6VP60xdodM>.b4KTZE9QYRS3GBc4f8oH .a9nFpIr7oIn7BaeaRJNH,.KFMEJtkQQh6VP60xdodM>.b4KTZE9QYRS3GBc4f8oH .fmzPPQxcMhvDfItahiyF{border:1px solid var(--background-color);box-sizing:border-box;width:50px}.KFMEJtkQQh6VP60xdodM>.b4KTZE9QYRS3GBc4f8oH .fmzPPQxcMhvDfItahiyF{background-color:#c8d8e8;color:#185290;height:25px}.KFMEJtkQQh6VP60xdodM>.b4KTZE9QYRS3GBc4f8oH .fmzPPQxcMhvDfItahiyF:active{background-color:#013f7d;color:var(--background-color)}.KFMEJtkQQh6VP60xdodM>.b4KTZE9QYRS3GBc4f8oH .ulwP_8htCQL74O1U1CDC{background-color:#333;border:1px solid var(--background-color);color:var(--background-color)}.KFMEJtkQQh6VP60xdodM>.b4KTZE9QYRS3GBc4f8oH .ulwP_8htCQL74O1U1CDC:active{background-color:#aaa;color:var(--foreground-color)}.KFMEJtkQQh6VP60xdodM>.b4KTZE9QYRS3GBc4f8oH .I366TQT8_e8CzAyKCMnC{background-color:#ccc;border:1px solid var(--background-color);color:#333}.KFMEJtkQQh6VP60xdodM>.b4KTZE9QYRS3GBc4f8oH .I366TQT8_e8CzAyKCMnC:active{background-color:var(--foreground-color);color:var(--background-color)}.KFMEJtkQQh6VP60xdodM>.b4KTZE9QYRS3GBc4f8oH .VRPHnV6mSFxflptcS6Io{color:#262626;display:table-cell;font-size:.8em;text-align:center;vertical-align:middle;width:100px}.KFMEJtkQQh6VP60xdodM>.b4KTZE9QYRS3GBc4f8oH .c1bD0W8VsWMksGGHY_GI{background-color:#dcadb0;border:1px solid var(--background-color);color:red}.KFMEJtkQQh6VP60xdodM>.b4KTZE9QYRS3GBc4f8oH .c1bD0W8VsWMksGGHY_GI:active{background-color:red;color:var(--background-color)}.KFMEJtkQQh6VP60xdodM>.b4KTZE9QYRS3GBc4f8oH .heI0aGKWnCQpDO1BLJvm,.KFMEJtkQQh6VP60xdodM>.b4KTZE9QYRS3GBc4f8oH .Vk8eT5pVqqv2M_TX597w{display:inline-block}.KFMEJtkQQh6VP60xdodM>.b4KTZE9QYRS3GBc4f8oH sup{font-size:smaller;vertical-align:super}.KFMEJtkQQh6VP60xdodM>.b4KTZE9QYRS3GBc4f8oH input[type=radio]{font-size:1em;margin:0;opacity:0;padding:0;width:25px}.KFMEJtkQQh6VP60xdodM>.b4KTZE9QYRS3GBc4f8oH input[type=radio]+label{display:inline-block;line-height:1.5em;margin-left:-2em}.KFMEJtkQQh6VP60xdodM>.b4KTZE9QYRS3GBc4f8oH input[type=radio]+label>span{background:#e0e0e0;background-image:linear-gradient(#f0f0f0,#e0e0e0);border:.0625em solid silver;border-radius:2px;display:inline-block;height:12px;margin:2px;vertical-align:bottom;width:12px}.KFMEJtkQQh6VP60xdodM>.b4KTZE9QYRS3GBc4f8oH input[type=radio]:checked+label>span{background-image:linear-gradient(#e0e0e0,#f0f0f0)}.KFMEJtkQQh6VP60xdodM>.b4KTZE9QYRS3GBc4f8oH input[type=radio]:checked+label>span>span{background:#9c6;background-image:linear-gradient(#b3d98c,#9c6);border:.0625em solid #73994d;border-radius:2px;display:block;height:6px;margin:2px;width:6px}.KFMEJtkQQh6VP60xdodM>.b4KTZE9QYRS3GBc4f8oH input[type=radio i]{-webkit-appearance:radio;-moz-appearance:radio;appearance:radio;box-sizing:border-box}",
            ""
          ]), d.locals = {
            calc: "KFMEJtkQQh6VP60xdodM",
            header: "MaG6OfsVlubNNO4TeoRQ",
            title: "pNQCYApFqkn5N4pvFmYn",
            close_btn: "wnN5ha1YAuW5AiVg6NGX",
            body: "b4KTZE9QYRS3GBc4f8oH",
            input: "tMJ6stmo6_eewwnrQYtg",
            output: "I2iV3n5EHDtHhDyLhiqP",
            block: "qyFAAcsJGzEmmG4p73Lm",
            line: "MGe5iZTkFHemhqzswxPK",
            rfunc: "a9nFpIr7oIn7BaeaRJNH",
            scifunc: "fmzPPQxcMhvDfItahiyF",
            scinm: "ulwP_8htCQL74O1U1CDC",
            sciop: "I366TQT8_e8CzAyKCMnC",
            scird: "VRPHnV6mSFxflptcS6Io",
            scieq: "c1bD0W8VsWMksGGHY_GI",
            scirdsettingd: "heI0aGKWnCQpDO1BLJvm",
            scirdsettingr: "Vk8eT5pVqqv2M_TX597w"
          };
          const p = d
        },
        5501: (e, t, r) => {
          r.d(t, {
            Z: () => f
          });
          var i = r(9601),
            n = r.n(i),
            o = r(2609),
            a = r.n(o),
            s = r(8991),
            c = r.n(s),
            l = new URL(r(8632), r.b),
            d = new URL(r(6323), r.b),
            u = new URL(r(7521), r.b),
            p = new URL(r(9046), r.b),
            v = a()(n()),
            m = c()(l),
            h = c()(d),
            g = c()(u),
            b = c()(p);
          v.push([e.id,
            ".humRkf1V9kt1b8mwO1eh{background:var(--background-color);border-radius:3px;bottom:2px;box-shadow:0 0 3px 0 rgba(0,0,0,.5);display:flex;flex:auto;flex-direction:column;overflow:hidden;position:fixed;right:2px;top:2px;visibility:visible;width:300px;z-index:1}.f3alWB8Tb5Es1kB1DzaW{align-items:center;background:var(--primary-color);display:flex;font-weight:700;padding:10px 15px;white-space:nowrap}.f3alWB8Tb5Es1kB1DzaW .KY98IJbLuFo9suLcGU4Q{color:var(--background-color);cursor:default;flex:1;font-weight:700}.f3alWB8Tb5Es1kB1DzaW ._0iu9rkKdU62jnWGOQQw{background:50%/50% var(--background-color) url(" +
            m +
            ") no-repeat;border-radius:50%;cursor:pointer;height:20px;min-height:20px;min-width:20px;opacity:1;width:20px}.f3alWB8Tb5Es1kB1DzaW ._0iu9rkKdU62jnWGOQQw:hover{opacity:.8}.hSme9E3rFWFKx2bD2X6V{background:var(--background-color);border-top:1px solid var(--secondary-color)}.hSme9E3rFWFKx2bD2X6V .PhrHIc12uP5ElSHBpZhS{align-items:center;display:flex;margin:8px 4px}.hSme9E3rFWFKx2bD2X6V .PhrHIc12uP5ElSHBpZhS>div{margin:0 4px}.hSme9E3rFWFKx2bD2X6V .VouY7x6stT6uVvvid2tx{border:1px solid var(--secondary-color);border-radius:3px;color:var(--background-color);cursor:default;flex:auto;font-size:.8em;overflow:hidden;padding:0 8px;position:relative;white-space:nowrap}.hSme9E3rFWFKx2bD2X6V .rRSruXMgD92dnTHvgEkp{background-color:var(--primary-color);bottom:0;height:100%;left:0;position:absolute;right:0;top:0;z-index:-1}.hSme9E3rFWFKx2bD2X6V .Xr7YIH1MR9YV_zJGLU2s{background-color:var(--success-color)}.hSme9E3rFWFKx2bD2X6V .tKE4PzHPrg1DdyNEmtjW{background-color:var(--danger-color)}.mYnl9e7i7lCsOGgQm6iF{background:50%/100% transparent url(" +
            h +
            ") no-repeat;height:1em;width:1em}.hSme9E3rFWFKx2bD2X6V .Xvmqsi37qKxUhB7UsTr6{background:50%/75% transparent url(" +
            m +
            ") no-repeat;cursor:pointer;height:1em;opacity:1;width:1em}.hSme9E3rFWFKx2bD2X6V .Xvmqsi37qKxUhB7UsTr6:hover{opacity:.8}.N6v3wExCM5w5ouXLY6n3{border-bottom:1px solid var(--secondary-color);flex:1;max-height:200px;position:relative}.N6v3wExCM5w5ouXLY6n3:empty{display:none}.MkFl232xeIkTKyBl9VV7{background:var(--background-color);flex:1;min-height:80px;overflow-y:auto}.MkFl232xeIkTKyBl9VV7:empty{background:50%/30% transparent url(" +
            g +
            ") no-repeat}.MkFl232xeIkTKyBl9VV7 .UcWkUK45T002X24kf5VE{background-color:hsla(0,0%,50%,.05);border-color:var(--primary-color);border-bottom:1px solid var(--secondary-color);border-left-style:solid;border-left-width:3px;border-radius:3px;border-right-style:solid;border-right-width:3px;border-top:1px solid var(--secondary-color);display:block;font-size:1em;margin:4px;overflow:hidden;padding:5px 10px;word-break:break-word}.MkFl232xeIkTKyBl9VV7 .UcWkUK45T002X24kf5VE.qIYBaPVYxrZsEA3jBNrh{border-left-color:var(--primary-color);border-right-color:var(--secondary-color)}.MkFl232xeIkTKyBl9VV7 .UcWkUK45T002X24kf5VE.QizGFmHlEUGpHoxJo9jN{border-left-color:var(--secondary-color);border-right-color:var(--primary-color)}.MkFl232xeIkTKyBl9VV7 .UcWkUK45T002X24kf5VE.nR9XqrApwVmS86ikU_Hh{background-color:rgba(191,64,64,.1)}.MkFl232xeIkTKyBl9VV7 .UcWkUK45T002X24kf5VE>.uADvPNIBjlh_wMFhz5ks{display:flex;margin-bottom:5px;opacity:.5}.MkFl232xeIkTKyBl9VV7 .UcWkUK45T002X24kf5VE>.uADvPNIBjlh_wMFhz5ks>.QZjD2ydct0oH2GHzbJGa{flex:1;font-size:.9em;font-weight:700;overflow:hidden;white-space:nowrap}.MkFl232xeIkTKyBl9VV7 .UcWkUK45T002X24kf5VE>.uADvPNIBjlh_wMFhz5ks>.X2gHXlAEl0L_IO91QgUp,.MkFl232xeIkTKyBl9VV7 .UcWkUK45T002X24kf5VE>.uADvPNIBjlh_wMFhz5ks>.QZjD2ydct0oH2GHzbJGa{color:var(--foreground-color);display:inline-block;vertical-align:middle}.MkFl232xeIkTKyBl9VV7 .UcWkUK45T002X24kf5VE>.uADvPNIBjlh_wMFhz5ks>.X2gHXlAEl0L_IO91QgUp{font-size:.6em;line-height:.8em;margin:auto 4px;padding:2px}.MkFl232xeIkTKyBl9VV7 .UcWkUK45T002X24kf5VE>.ULQit6h8sz5Xv63kvFNQ{display:block}.MkFl232xeIkTKyBl9VV7 .UcWkUK45T002X24kf5VE>.ULQit6h8sz5Xv63kvFNQ .PBiJbX4jTqx9StMJgUxu{color:var(--foreground-color);display:inline-block;white-space:pre-wrap}.MkFl232xeIkTKyBl9VV7 .UcWkUK45T002X24kf5VE>.ULQit6h8sz5Xv63kvFNQ .kspe4Ir5loW9bEL9IJKz{display:inline}.MkFl232xeIkTKyBl9VV7 .UcWkUK45T002X24kf5VE>.ULQit6h8sz5Xv63kvFNQ .CFn2ttx4MLhot_R3lXiF{display:block}.MkFl232xeIkTKyBl9VV7 .UcWkUK45T002X24kf5VE>.ULQit6h8sz5Xv63kvFNQ img,.MkFl232xeIkTKyBl9VV7 .UcWkUK45T002X24kf5VE>.ULQit6h8sz5Xv63kvFNQ video{border:1px solid var(--secondary-color);box-sizing:border-box;max-width:100%;object-fit:contain}.gJRY3W0lV8bLveL0_ebG{background:var(--secondary-color);display:flex;min-height:50px;padding:8px}.gJRY3W0lV8bLveL0_ebG .Edzl1JrXiyL2fwN1K1fT{align-self:center}.gJRY3W0lV8bLveL0_ebG textarea.Tn5uaoliIxyJIt4lOixe{flex:1;margin-right:6px}.gJRY3W0lV8bLveL0_ebG .aUKKyOVQ4Y84MbNx5jDJ{background:50%/60% transparent url(" +
            b +
            ") no-repeat;cursor:pointer;display:block;height:32px;opacity:1;width:32px}.gJRY3W0lV8bLveL0_ebG .aUKKyOVQ4Y84MbNx5jDJ:hover{opacity:.8}.gJRY3W0lV8bLveL0_ebG .WauO7Sd1jwBkcDN25yyo{background:50%/60% transparent url(" +
            h +
            ") no-repeat;cursor:pointer;display:block;height:32px;opacity:1;width:32px}.gJRY3W0lV8bLveL0_ebG .WauO7Sd1jwBkcDN25yyo:hover{opacity:.8}.gJRY3W0lV8bLveL0_ebG .oUBoJ7glGitTccwQaJIW{display:none}@media only screen and (max-width:300px){.humRkf1V9kt1b8mwO1eh{left:2px;width:auto}}@media only screen and (orientation:portrait){.humRkf1V9kt1b8mwO1eh{left:2px;width:auto}}",
            ""
          ]), v.locals = {
            chat: "humRkf1V9kt1b8mwO1eh",
            header: "f3alWB8Tb5Es1kB1DzaW",
            title: "KY98IJbLuFo9suLcGU4Q",
            close_btn: "_0iu9rkKdU62jnWGOQQw",
            files: "hSme9E3rFWFKx2bD2X6V",
            file: "PhrHIc12uP5ElSHBpZhS",
            filename: "VouY7x6stT6uVvvid2tx",
            progress: "rRSruXMgD92dnTHvgEkp",
            progress_done: "Xr7YIH1MR9YV_zJGLU2s",
            progress_err: "tKE4PzHPrg1DdyNEmtjW",
            attach_icon: "mYnl9e7i7lCsOGgQm6iF",
            remove: "Xvmqsi37qKxUhB7UsTr6",
            player: "N6v3wExCM5w5ouXLY6n3",
            body: "MkFl232xeIkTKyBl9VV7",
            item: "UcWkUK45T002X24kf5VE",
            left: "qIYBaPVYxrZsEA3jBNrh",
            right: "QizGFmHlEUGpHoxJo9jN",
            highlight: "nR9XqrApwVmS86ikU_Hh",
            caption: "uADvPNIBjlh_wMFhz5ks",
            user: "QZjD2ydct0oH2GHzbJGa",
            time: "X2gHXlAEl0L_IO91QgUp",
            message: "ULQit6h8sz5Xv63kvFNQ",
            text: "PBiJbX4jTqx9StMJgUxu",
            link: "kspe4Ir5loW9bEL9IJKz",
            attach: "CFn2ttx4MLhot_R3lXiF",
            footer: "gJRY3W0lV8bLveL0_ebG",
            buttons: "Edzl1JrXiyL2fwN1K1fT",
            input_text: "Tn5uaoliIxyJIt4lOixe",
            send_btn: "aUKKyOVQ4Y84MbNx5jDJ",
            clip_btn: "WauO7Sd1jwBkcDN25yyo",
            input_file: "oUBoJ7glGitTccwQaJIW"
          };
          const f = v
        },
        9461: (e, t, r) => {
          r.d(t, {
            Z: () => s
          });
          var i = r(9601),
            n = r.n(i),
            o = r(2609),
            a = r.n(o)()(n());
          a.push([e.id,
            ".G73rvDlo3YYf4MtqeKCX{display:flex;height:100%}.UP5_GAum5cvIcMEgYy30{padding:20px;width:40%}.kdVph7O6dG6i_ebNrYik{border-left:1px solid var(--secondary-color);margin:20px 0}.XL_lZwON6lIRCJ2n8BmF{flex:1;padding:20px}.XL_lZwON6lIRCJ2n8BmF>.vrvnV1E0gfBr_klz9EQn{display:flex;flex-direction:column;padding-bottom:20px}.XL_lZwON6lIRCJ2n8BmF>.vrvnV1E0gfBr_klz9EQn>.NrXcoIdWo7Ms66IINKnz{color:var(--danger-color);font-size:.9em;padding:10px}.XL_lZwON6lIRCJ2n8BmF>.vrvnV1E0gfBr_klz9EQn>.NrXcoIdWo7Ms66IINKnz>.sxoBoQm3x7WJ3aAFA1i0{background-color:var(--danger-color);display:block;margin-top:10px;padding:4px 10px}.XL_lZwON6lIRCJ2n8BmF>.vrvnV1E0gfBr_klz9EQn>.NrXcoIdWo7Ms66IINKnz>.sxoBoQm3x7WJ3aAFA1i0>span{color:var(--background-color)}.XL_lZwON6lIRCJ2n8BmF>.vrvnV1E0gfBr_klz9EQn>.sk4Mt1Q2iV1yFMw6zTGk>.JXjyQ0cXENhZE_O9E0Ea{border-radius:50%;display:inline-block;margin:0 8px;padding:6px;vertical-align:middle}.XL_lZwON6lIRCJ2n8BmF>.vrvnV1E0gfBr_klz9EQn>.sk4Mt1Q2iV1yFMw6zTGk>.KjQqn8pb5VXEBys0ACsp{color:var(--foreground-color);vertical-align:middle}.XL_lZwON6lIRCJ2n8BmF>.vrvnV1E0gfBr_klz9EQn>.sk4Mt1Q2iV1yFMw6zTGk>.W94h9wzbLqj5yMco7wTe{background-color:var(--info-color)}.XL_lZwON6lIRCJ2n8BmF>.vrvnV1E0gfBr_klz9EQn>.sk4Mt1Q2iV1yFMw6zTGk>.QKSt1YwLuNmE_indxzPr{background-color:var(--success-color)}.XL_lZwON6lIRCJ2n8BmF>.vrvnV1E0gfBr_klz9EQn>.sk4Mt1Q2iV1yFMw6zTGk>.YNsFhJRb3A0cAsJ33yux{background-color:var(--danger-color)}.XL_lZwON6lIRCJ2n8BmF>.vrvnV1E0gfBr_klz9EQn>.sk4Mt1Q2iV1yFMw6zTGk>.ttdZPYb01sOAQ1pFOotS{animation:EDpvxDHMN3yzyzVbYxli 1s linear infinite;background-color:var(--warning-color)}@keyframes EDpvxDHMN3yzyzVbYxli{0%{opacity:1}50%{opacity:.1}to{opacity:1}}@media only screen and (orientation:portrait){.UP5_GAum5cvIcMEgYy30,.kdVph7O6dG6i_ebNrYik{display:none}}",
            ""
          ]), a.locals = {
            check: "G73rvDlo3YYf4MtqeKCX",
            description: "UP5_GAum5cvIcMEgYy30",
            separator: "kdVph7O6dG6i_ebNrYik",
            body: "XL_lZwON6lIRCJ2n8BmF",
            item: "vrvnV1E0gfBr_klz9EQn",
            msg: "NrXcoIdWo7Ms66IINKnz",
            retry_btn: "sxoBoQm3x7WJ3aAFA1i0",
            label: "sk4Mt1Q2iV1yFMw6zTGk",
            icon: "JXjyQ0cXENhZE_O9E0Ea",
            text: "KjQqn8pb5VXEBys0ACsp",
            ready: "W94h9wzbLqj5yMco7wTe",
            passed: "QKSt1YwLuNmE_indxzPr",
            error: "YNsFhJRb3A0cAsJ33yux",
            active: "ttdZPYb01sOAQ1pFOotS",
            blink: "EDpvxDHMN3yzyzVbYxli"
          };
          const s = a
        },
        8512: (e, t, r) => {
          r.d(t, {
            Z: () => O
          });
          var i = r(9601),
            n = r.n(i),
            o = r(2609),
            a = r.n(o),
            s = r(8991),
            c = r.n(s),
            l = new URL(r(8260), r.b),
            d = new URL(r(1686), r.b),
            u = new URL(r(3824), r.b),
            p = new URL(r(8160), r.b),
            v = new URL(r(1952), r.b),
            m = new URL(r(2583), r.b),
            h = new URL(r(4561), r.b),
            g = new URL(r(5746), r.b),
            b = new URL(r(4541), r.b),
            f = new URL(r(2158), r.b),
            y = new URL(r(6712), r.b),
            M = new URL(r(368), r.b),
            j = new URL(r(390), r.b),
            P = a()(n()),
            T = c()(l),
            L = c()(d),
            A = c()(u),
            w = c()(p),
            k = c()(v),
            N = c()(m),
            I = c()(h),
            D = c()(g),
            C = c()(b),
            z = c()(f),
            x = c()(y),
            E = c()(M),
            S = c()(j);
          P.push([e.id,
            ".e1ROklbcqo1zcKzPlRBn{grid-gap:1px;background-color:#444;bottom:0;display:grid;font-family:Arial,Helvetica,sans-serif;height:100%;left:0;position:absolute;right:0;top:0;width:100%}.e1ROklbcqo1zcKzPlRBn.qidrb4teUZACVzPmMu6u{bottom:0;left:0;max-height:none;position:fixed;right:0;top:0;z-index:1}.UE7Hv3w5TQtqyYAtaqMO{display:flex;flex-direction:column;overflow:hidden;position:relative}.UE7Hv3w5TQtqyYAtaqMO:before{content:attr(data-title)}.UE7Hv3w5TQtqyYAtaqMO[data-maximized=true]{bottom:0;left:0;position:absolute;right:0;top:0;z-index:3}.dAyNCmbsWfoG943sr1xf>video{background-color:#000;height:100%;object-fit:contain;width:100%}.dAyNCmbsWfoG943sr1xf>video[data-mirror]{transform:rotateY(180deg)}.dAyNCmbsWfoG943sr1xf>video[data-spinner]{background-image:url(" +
            T +
            ");background-position:50%;background-repeat:no-repeat;background-size:auto;transform:none}.dAyNCmbsWfoG943sr1xf:not([data-selected]){border:1px solid hsla(0,0%,50%,.5);border-radius:3px;cursor:pointer;line-height:0;margin:2px;max-height:100%;max-width:20%;position:relative;z-index:1}.dAyNCmbsWfoG943sr1xf[data-selected]{bottom:0;left:0;position:absolute;right:0;top:0;z-index:0}.UE7Hv3w5TQtqyYAtaqMO[data-single=true]>.dAyNCmbsWfoG943sr1xf:not([data-selected]){display:none}.LSbUaUUIfuIQAzDvh6b0{background-color:rgba(30,30,30,.9);border-top:1px solid #444;bottom:0;color:#fff;display:flex;font-size:14px;height:28px;line-height:28px;opacity:.8;overflow:hidden;position:absolute;width:100%;z-index:2}.e1ROklbcqo1zcKzPlRBn:not(.qidrb4teUZACVzPmMu6u) .LSbUaUUIfuIQAzDvh6b0{opacity:0;transition:opacity .3s ease-out 2s}.UE7Hv3w5TQtqyYAtaqMO:hover .LSbUaUUIfuIQAzDvh6b0{opacity:.8;transition:none}.kgjmOmgvObBzbl34DnLk{margin-left:10px;overflow:hidden;width:100%}.v7ZK_weNiRPASKafuPNw{cursor:pointer;opacity:.9;padding:0 8px;text-align:center}.v7ZK_weNiRPASKafuPNw:hover{background-color:rgba(0,0,0,.4);opacity:1}.UE7Hv3w5TQtqyYAtaqMO .YQ2rb7qGz6892Zn9O0GJ{background-image:url(" +
            L +
            ");background-position:50%;background-repeat:no-repeat;background-size:contain;display:inline-block;height:100%;width:16px}.UE7Hv3w5TQtqyYAtaqMO[data-single=true] .YQ2rb7qGz6892Zn9O0GJ{background-image:url(" +
            A + ")}.UE7Hv3w5TQtqyYAtaqMO .ZQVkopcAKkTAAyPqJMDr{background-image:url(" + w +
            ");background-position:50%;background-repeat:no-repeat;background-size:contain;display:inline-block;height:100%;width:16px}.UE7Hv3w5TQtqyYAtaqMO[data-muted=true] .ZQVkopcAKkTAAyPqJMDr{background-image:url(" +
            k + ")}.UE7Hv3w5TQtqyYAtaqMO .mhJg1GNWomxVriXamao0{background-image:url(" + N +
            ");background-position:50%;background-repeat:no-repeat;background-size:contain;display:inline-block;height:100%;width:16px}.UE7Hv3w5TQtqyYAtaqMO[data-maximized=true] .mhJg1GNWomxVriXamao0{background-image:url(" +
            I + ")}.UE7Hv3w5TQtqyYAtaqMO .CdpeeQldkT1XC8iE1kEU{background-image:url(" + D +
            ");background-position:50%;background-repeat:no-repeat;background-size:contain;display:inline-block;height:100%;width:16px}.UE7Hv3w5TQtqyYAtaqMO[data-microphone=true] .CdpeeQldkT1XC8iE1kEU{background-image:url(" +
            C + ")}.UE7Hv3w5TQtqyYAtaqMO .ubnPIEIXR54TvIYUu49c{background-image:url(" + z +
            ");background-position:50%;background-repeat:no-repeat;background-size:contain;display:inline-block;height:100%;width:16px}.UE7Hv3w5TQtqyYAtaqMO[data-camera=true] .ubnPIEIXR54TvIYUu49c{background-image:url(" +
            x + ")}.UE7Hv3w5TQtqyYAtaqMO .dJH4NbJbUe6Zle9tvw2w{background-image:url(" + E +
            ");background-position:50%;background-repeat:no-repeat;background-size:contain;display:inline-block;height:100%;width:16px}.UE7Hv3w5TQtqyYAtaqMO[data-screen=true] .dJH4NbJbUe6Zle9tvw2w{background-image:url(" +
            S + ")}", ""
          ]), P.locals = {
            conference_level1: "e1ROklbcqo1zcKzPlRBn",
            expanded: "qidrb4teUZACVzPmMu6u",
            conference_level2: "UE7Hv3w5TQtqyYAtaqMO",
            conference_level3: "dAyNCmbsWfoG943sr1xf",
            conference_footer: "LSbUaUUIfuIQAzDvh6b0",
            conference_text: "kgjmOmgvObBzbl34DnLk",
            conference_button: "v7ZK_weNiRPASKafuPNw",
            single_btn: "YQ2rb7qGz6892Zn9O0GJ",
            mute_btn: "ZQVkopcAKkTAAyPqJMDr",
            maximize_btn: "mhJg1GNWomxVriXamao0",
            microphone_btn: "CdpeeQldkT1XC8iE1kEU",
            camera_btn: "ubnPIEIXR54TvIYUu49c",
            screen_btn: "dJH4NbJbUe6Zle9tvw2w"
          };
          const O = P
        },
        8365: (e, t, r) => {
          r.d(t, {
            Z: () => s
          });
          var i = r(9601),
            n = r.n(i),
            o = r(2609),
            a = r.n(o)()(n());
          a.push([e.id,
            '.UlhzgCFDOCfnTCaPUzdQ{display:flex;flex-direction:column;justify-content:center;margin:auto;padding:15px;width:75%}.m9Kgsv9EDREKJAIRGrfb{border-bottom:1px solid var(--secondery-color);font-weight:700;margin-bottom:15px;text-transform:uppercase}.m9Kgsv9EDREKJAIRGrfb,.i1EdbWOWFS7msRfqKI_3{color:var(--foreground-color);display:block}.x_Ak4TNROIgfH7g_l8tR{background-color:var(--background-color);cursor:pointer;display:block;margin-top:30px;padding:5px 5px 5px 40px;position:relative;-webkit-user-select:none;-moz-user-select:none;user-select:none}.x_Ak4TNROIgfH7g_l8tR .Ht6LxG8oEbKWKYIEO6ur{color:var(--foreground-color)}.x_Ak4TNROIgfH7g_l8tR input{cursor:pointer;height:0;opacity:0;position:absolute;width:0}.x_Ak4TNROIgfH7g_l8tR .yy7b6Ydgnn6TxYxr18Nw{background-color:var(--background-color);border:1px solid var(--primary-color);border-radius:3px;bottom:0;height:20px;left:5px;margin:auto;position:absolute;top:0;width:20px}.x_Ak4TNROIgfH7g_l8tR input:checked~.yy7b6Ydgnn6TxYxr18Nw{background-color:var(--primary-color)}.x_Ak4TNROIgfH7g_l8tR .yy7b6Ydgnn6TxYxr18Nw:after{border:solid var(--background-color);border-width:0 3px 3px 0;box-sizing:initial;content:"";display:none;height:10px;left:6px;position:absolute;top:2px;transform:rotate(45deg);width:5px}.x_Ak4TNROIgfH7g_l8tR input:checked~.yy7b6Ydgnn6TxYxr18Nw:after{display:block}',
            ""
          ]), a.locals = {
            content: "UlhzgCFDOCfnTCaPUzdQ",
            label: "m9Kgsv9EDREKJAIRGrfb",
            text: "i1EdbWOWFS7msRfqKI_3",
            checkbox: "x_Ak4TNROIgfH7g_l8tR",
            caption: "Ht6LxG8oEbKWKYIEO6ur",
            checkmark: "yy7b6Ydgnn6TxYxr18Nw"
          };
          const s = a
        },
        9561: (e, t, r) => {
          r.d(t, {
            Z: () => p
          });
          var i = r(9601),
            n = r.n(i),
            o = r(2609),
            a = r.n(o),
            s = r(8991),
            c = r.n(s),
            l = new URL(r(8632), r.b),
            d = a()(n()),
            u = c()(l);
          d.push([e.id,
            ".Jjih1sxZ0HyCp22KRdhc{background:var(--background);display:block}.YbdF6AdMRStjluicNtsg,.Jjih1sxZ0HyCp22KRdhc{bottom:0;left:0;position:inherit;right:0;top:0;visibility:visible}.YbdF6AdMRStjluicNtsg{background:var(--background-color);border-radius:3px;box-shadow:0 0 3px 0 rgba(0,0,0,.5);display:flex;flex-direction:column;height:480px;margin:auto;max-height:100vh;max-width:100vw;overflow:hidden;width:700px}.cmVCeSmVSLowlkyzzb7V{align-items:center;background:var(--primary-color);display:flex;font-weight:700;padding:10px 15px;white-space:nowrap}.cmVCeSmVSLowlkyzzb7V:empty{display:none}.cmVCeSmVSLowlkyzzb7V .sRl_ZGZuM5A4Td3vhp99{color:var(--background-color);cursor:default;flex:1}.cmVCeSmVSLowlkyzzb7V .zbMqOciFBfwSXGpXIbVz{background:50%/50% var(--background-color) url(" +
            u +
            ") no-repeat;border-radius:50%;cursor:pointer;height:20px;min-height:20px;min-width:20px;opacity:1;visibility:var(--dialog-close-btn);width:20px}.cmVCeSmVSLowlkyzzb7V .zbMqOciFBfwSXGpXIbVz:hover{opacity:.8}.I1s3cXfZ4x6kluDy1qCP{background:var(--background-color);display:flex;flex:1;flex-direction:column;overflow:auto}.I1s3cXfZ4x6kluDy1qCP>div{flex:1}.gklCMwQ_YcHptgw4rtNm{align-items:center;background:var(--secondary-color);display:flex;padding:10px}.gklCMwQ_YcHptgw4rtNm:empty{display:none}.gklCMwQ_YcHptgw4rtNm .rvun84YXTpR5devgXEIw{color:var(--foreground-color);flex:1;opacity:.5;padding:8px 10px;text-align:left;white-space:nowrap}.gklCMwQ_YcHptgw4rtNm button.r6fP0si7qVHBEAFeNFtI{background-color:var(--success-color);margin:0 2px;width:120px}.gklCMwQ_YcHptgw4rtNm button.Kn3s1bhxnmhA4kyWjlKP{background-color:var(--danger-color);margin:0 2px;width:120px}",
            ""
          ]), d.locals = {
            dialog: "Jjih1sxZ0HyCp22KRdhc",
            container: "YbdF6AdMRStjluicNtsg",
            header: "cmVCeSmVSLowlkyzzb7V",
            title: "sRl_ZGZuM5A4Td3vhp99",
            close_btn: "zbMqOciFBfwSXGpXIbVz",
            body: "I1s3cXfZ4x6kluDy1qCP",
            footer: "gklCMwQ_YcHptgw4rtNm",
            caption: "rvun84YXTpR5devgXEIw",
            ok_btn: "r6fP0si7qVHBEAFeNFtI",
            cancel_btn: "Kn3s1bhxnmhA4kyWjlKP"
          };
          const p = d
        },
        8597: (e, t, r) => {
          r.d(t, {
            Z: () => p
          });
          var i = r(9601),
            n = r.n(i),
            o = r(2609),
            a = r.n(o),
            s = r(8991),
            c = r.n(s),
            l = new URL(r(3698), r.b),
            d = a()(n()),
            u = c()(l);
          d.push([e.id,
            ".R2duYUVtys7SoOX2f9xQ{display:flex;height:100%}.jwBDY0Bje_m4wGeSAzAI{padding:20px;width:40%}.a37PZU4xp7A9mOy7lEFj{border-left:1px solid var(--secondary-color);margin:20px 0}.anitebgTfzi2aYYzE911{display:flex;flex:1;flex-direction:column;padding:20px;position:relative}.anitebgTfzi2aYYzE911 .xM6jDVQXkrrZwVicTzf3{background-color:#000;border-top-left-radius:3px;border-top-right-radius:3px;flex:1;overflow:hidden;position:relative}.anitebgTfzi2aYYzE911 .GC_ih64ah7EtxDZqyR3W{height:100%;margin-left:auto;margin-right:auto;object-fit:contain;width:100%}.anitebgTfzi2aYYzE911 .y2ddBQIzl6R1910bW3NW,.anitebgTfzi2aYYzE911 .GC_ih64ah7EtxDZqyR3W{bottom:0;left:0;position:absolute;right:0;top:0}.anitebgTfzi2aYYzE911 .y2ddBQIzl6R1910bW3NW:empty{background-image:url(" +
            u +
            ");background-position:50%;background-repeat:no-repeat;background-size:contain}.anitebgTfzi2aYYzE911 .y2ddBQIzl6R1910bW3NW:not(:empty){background-color:rgba(0,0,0,.5);color:#fff;font-size:.8em;overflow-x:auto;padding:10px}.anitebgTfzi2aYYzE911 .y2ddBQIzl6R1910bW3NW p{display:block;padding:5px}.anitebgTfzi2aYYzE911 .y2ddBQIzl6R1910bW3NW b{font-weight:700}.anitebgTfzi2aYYzE911 .y2ddBQIzl6R1910bW3NW li{display:list-item;margin-left:20px}.anitebgTfzi2aYYzE911 .cydVGFV_l4RqP0PGgtC3{border-radius:3px;border-top-left-radius:0;border-top-right-radius:0;display:flex;overflow:hidden}.anitebgTfzi2aYYzE911 .cydVGFV_l4RqP0PGgtC3 button.MUh08_6ylY_G8r22kkEg,.anitebgTfzi2aYYzE911 .cydVGFV_l4RqP0PGgtC3 button.em6hGz7ZXvyUMAEbUBrA{background-color:#000;border:1px solid #333;border-radius:0;color:#fff;flex:1;font-weight:700;text-transform:uppercase;white-space:nowrap}.anitebgTfzi2aYYzE911 .cydVGFV_l4RqP0PGgtC3 button.XnGeorgDOiR3mUsx3SUM{display:none}@media only screen and (orientation:portrait){.jwBDY0Bje_m4wGeSAzAI,.a37PZU4xp7A9mOy7lEFj{display:none}}",
            ""
          ]), d.locals = {
            face: "R2duYUVtys7SoOX2f9xQ",
            description: "jwBDY0Bje_m4wGeSAzAI",
            separator: "a37PZU4xp7A9mOy7lEFj",
            body: "anitebgTfzi2aYYzE911",
            preview: "xM6jDVQXkrrZwVicTzf3",
            webcam: "GC_ih64ah7EtxDZqyR3W",
            overlay: "y2ddBQIzl6R1910bW3NW",
            buttons: "cydVGFV_l4RqP0PGgtC3",
            retry_btn: "MUh08_6ylY_G8r22kkEg",
            take_btn: "em6hGz7ZXvyUMAEbUBrA",
            hidden: "XnGeorgDOiR3mUsx3SUM"
          };
          const p = d
        },
        9870: (e, t, r) => {
          r.d(t, {
            Z: () => f
          });
          var i = r(9601),
            n = r.n(i),
            o = r(2609),
            a = r.n(o),
            s = r(8991),
            c = r.n(s),
            l = new URL(r(3244), r.b),
            d = new URL(r(4400), r.b),
            u = new URL(r(7922), r.b),
            p = new URL(r(2675), r.b),
            v = a()(n()),
            m = c()(l),
            h = c()(d),
            g = c()(u),
            b = c()(p);
          v.push([e.id,
            ".iiFGRM5k__xnVUcovCMp{bottom:0;display:flex;flex-direction:column;left:0;position:inherit;right:0;top:0;visibility:visible;z-index:-1}.iiFGRM5k__xnVUcovCMp iframe{background:var(--background-color)}.NHzqc3AkagnS_B5lSQoB{-webkit-overflow-scrolling:touch;display:block;flex:auto;overflow:auto}.r9AyfM__JHMIdscOUtbB{background:var(--secondary-color);border-bottom:1px solid var(--primary-color);display:flex;padding:4px}.r9AyfM__JHMIdscOUtbB button.sUqLtrNbd6GtC6ojIhx3{-webkit-margin-start:10px;background-color:var(--danger-color);margin-inline-start:10px;min-width:100px}.yBDwZZfSnjIJp_u3P0Mn{color:var(--foreground-color);display:flex;flex:auto;flex-direction:column;font-size:.8em;justify-content:center;line-height:1.4em;overflow:hidden;padding:0 8px;white-space:nowrap}.yBDwZZfSnjIJp_u3P0Mn strong{font-weight:700}.fkFnuODHVueSWDAO35A1{background-color:initial;background-position:50%;background-repeat:no-repeat;background-size:100%;cursor:pointer;display:block;margin:10px;min-width:20px;opacity:.8;width:20px}.fkFnuODHVueSWDAO35A1:hover{opacity:.6}.fkFnuODHVueSWDAO35A1.BpIttoIUPb1AB7yP07Wn{background-image:url(" +
            m + ")}.fkFnuODHVueSWDAO35A1.SzLOA1AFwYRs81Jc7Vtz{background-image:url(" + h +
            ")}.fkFnuODHVueSWDAO35A1.H2fKHzSnk2BrxhfyHczq{background-image:url(" + g +
            ")}.fkFnuODHVueSWDAO35A1.kXAMQjub9uUn98fHLxOX{background-image:url(" + b + ")}", ""
          ]), v.locals = {
            iframe: "iiFGRM5k__xnVUcovCMp",
            body: "NHzqc3AkagnS_B5lSQoB",
            header: "r9AyfM__JHMIdscOUtbB",
            exit_btn: "sUqLtrNbd6GtC6ojIhx3",
            title: "yBDwZZfSnjIJp_u3P0Mn",
            btn: "fkFnuODHVueSWDAO35A1",
            home_btn: "BpIttoIUPb1AB7yP07Wn",
            chat_btn: "SzLOA1AFwYRs81Jc7Vtz",
            calc_btn: "H2fKHzSnk2BrxhfyHczq",
            qrcode_btn: "kXAMQjub9uUn98fHLxOX"
          };
          const f = v
        },
        4123: (e, t, r) => {
          r.d(t, {
            Z: () => s
          });
          var i = r(9601),
            n = r.n(i),
            o = r(2609),
            a = r.n(o)()(n());
          a.push([e.id,
            ".KFsVIQMPWmr6k3MAwEhG{display:flex;height:100%}.r5BCkn72u_ibFeozKOVQ{padding:20px;width:40%}.S0YlLzTpsc1bIDjSdLcv{border-left:1px solid var(--secondary-color);margin:20px 0}.C8XKKlB1_imlywmDr2Ib{padding:20px}.C8XKKlB1_imlywmDr2Ib,.C8XKKlB1_imlywmDr2Ib .lt8v4TbfYv6IL7m2CzQJ{display:flex;flex:1;position:relative}.C8XKKlB1_imlywmDr2Ib .lt8v4TbfYv6IL7m2CzQJ{flex-direction:column}.C8XKKlB1_imlywmDr2Ib .kjUFfA9ElAs0oW1B75IB{border:none;cursor:pointer;margin:auto;max-height:100%;max-width:100%;object-fit:contain}.C8XKKlB1_imlywmDr2Ib .oGOBboQROthMCcTdPish{background-color:#000;border-top-left-radius:3px;border-top-right-radius:3px;flex:1;overflow:hidden;position:relative}.C8XKKlB1_imlywmDr2Ib .KyXAnZZwAxaZh0rogyM4{bottom:0;height:100%;left:0;margin-left:auto;margin-right:auto;object-fit:contain;width:100%}.C8XKKlB1_imlywmDr2Ib .n9EcZz17UhJK3lx_2dCv,.C8XKKlB1_imlywmDr2Ib .KyXAnZZwAxaZh0rogyM4{position:absolute;right:0;top:0}.C8XKKlB1_imlywmDr2Ib .n9EcZz17UhJK3lx_2dCv{background-color:rgba(0,0,0,.5);border-radius:4px;color:#fff;display:none;font-weight:700;padding:5px 10px;width:-moz-fit-content;width:fit-content}.C8XKKlB1_imlywmDr2Ib .n9EcZz17UhJK3lx_2dCv:not(:empty){display:block}.C8XKKlB1_imlywmDr2Ib .HsELXy3wdUwRWNI6P8sl{bottom:0;display:none;left:0;position:absolute;right:0;top:0}.C8XKKlB1_imlywmDr2Ib .HsELXy3wdUwRWNI6P8sl:not(:empty){background-color:rgba(0,0,0,.5);color:#fff;display:block;font-size:.8em;overflow-x:auto;padding:10px}.C8XKKlB1_imlywmDr2Ib .HsELXy3wdUwRWNI6P8sl p{display:block;padding:5px}.C8XKKlB1_imlywmDr2Ib .HsELXy3wdUwRWNI6P8sl b{font-weight:700}.C8XKKlB1_imlywmDr2Ib .HsELXy3wdUwRWNI6P8sl li{display:list-item;margin-left:20px}.C8XKKlB1_imlywmDr2Ib .sz8Umxd5t7jwROkaSGCX{border-radius:3px;border-top-left-radius:0;border-top-right-radius:0;display:flex;overflow:hidden}.C8XKKlB1_imlywmDr2Ib .sz8Umxd5t7jwROkaSGCX button.MUZr7hz4_ssopuCs0xfO,.C8XKKlB1_imlywmDr2Ib .sz8Umxd5t7jwROkaSGCX button.iqJaHS2HXE33YY6cxkAb,.C8XKKlB1_imlywmDr2Ib .sz8Umxd5t7jwROkaSGCX button.uRq6ZTQNNv_AE3b6D3cW{background-color:#000;border:1px solid #333;border-radius:0;color:#fff;flex:1;font-weight:700;text-transform:uppercase;white-space:nowrap}.C8XKKlB1_imlywmDr2Ib .sz8Umxd5t7jwROkaSGCX button.BOC528V43iN9R6JRJVTQ,.C8XKKlB1_imlywmDr2Ib .BOC528V43iN9R6JRJVTQ{display:none}@media only screen and (orientation:portrait){.r5BCkn72u_ibFeozKOVQ,.S0YlLzTpsc1bIDjSdLcv{display:none}}",
            ""
          ]), a.locals = {
            overview: "KFsVIQMPWmr6k3MAwEhG",
            description: "r5BCkn72u_ibFeozKOVQ",
            separator: "S0YlLzTpsc1bIDjSdLcv",
            body: "C8XKKlB1_imlywmDr2Ib",
            recording: "lt8v4TbfYv6IL7m2CzQJ",
            qrcode: "kjUFfA9ElAs0oW1B75IB",
            preview: "oGOBboQROthMCcTdPish",
            webcam: "KyXAnZZwAxaZh0rogyM4",
            timer: "n9EcZz17UhJK3lx_2dCv",
            overlay: "HsELXy3wdUwRWNI6P8sl",
            buttons: "sz8Umxd5t7jwROkaSGCX",
            action_btn: "MUZr7hz4_ssopuCs0xfO",
            qrcode_btn: "iqJaHS2HXE33YY6cxkAb",
            retry_btn: "uRq6ZTQNNv_AE3b6D3cW",
            hidden: "BOC528V43iN9R6JRJVTQ"
          };
          const s = a
        },
        1156: (e, t, r) => {
          r.d(t, {
            Z: () => p
          });
          var i = r(9601),
            n = r.n(i),
            o = r(2609),
            a = r.n(o),
            s = r(8991),
            c = r.n(s),
            l = new URL(r(2894), r.b),
            d = a()(n()),
            u = c()(l);
          d.push([e.id,
            ".maifRQtxgpSscQm8oEQI{display:flex;height:100%}.SmCWLdwYU9nVmGKTxyLN{padding:20px;width:40%}.XHuJMjwtrufVRq9lFsqA{border-left:1px solid var(--secondary-color);margin:20px 0}.h99z3Q8GmSIKNBOeeAiG{display:flex;flex:1;flex-direction:column;padding:20px;position:relative}.h99z3Q8GmSIKNBOeeAiG .XTsf82b_Ippr6YQWXyFF{background-color:#000;border-top-left-radius:3px;border-top-right-radius:3px;flex:1;overflow:hidden;position:relative}.h99z3Q8GmSIKNBOeeAiG .KuLP9FswgqXlDXmRadny,.h99z3Q8GmSIKNBOeeAiG .cOzCl1KRsY7md_B1rfty{bottom:0;height:100%;left:0;margin-left:auto;margin-right:auto;object-fit:contain;position:absolute;right:0;top:0;width:100%}.h99z3Q8GmSIKNBOeeAiG .KuLP9FswgqXlDXmRadny:not([src]){display:none}.h99z3Q8GmSIKNBOeeAiG .GPYRmffxeDTiFyipo8zb{bottom:0;left:0;position:absolute;right:0;top:0}.h99z3Q8GmSIKNBOeeAiG .GPYRmffxeDTiFyipo8zb:empty{background-image:url(" +
            u +
            ");background-position:50%;background-repeat:no-repeat;background-size:contain}.h99z3Q8GmSIKNBOeeAiG .GPYRmffxeDTiFyipo8zb:not(:empty){background-color:rgba(0,0,0,.5);color:#fff;font-size:.8em;overflow-x:auto;padding:10px}.h99z3Q8GmSIKNBOeeAiG .GPYRmffxeDTiFyipo8zb p{display:block;padding:5px}.h99z3Q8GmSIKNBOeeAiG .GPYRmffxeDTiFyipo8zb b{font-weight:700}.h99z3Q8GmSIKNBOeeAiG .HlWbgLppOhZms_A9w6Z0{bottom:0;display:flex;left:0;position:absolute;right:0}.h99z3Q8GmSIKNBOeeAiG .HlWbgLppOhZms_A9w6Z0 .MlrKTF6MEFsY5CbvCVBK{border:1px solid var(--primary-color);display:block;height:60px;margin:2px;object-fit:contain;width:80px}.h99z3Q8GmSIKNBOeeAiG .HlWbgLppOhZms_A9w6Z0 .MlrKTF6MEFsY5CbvCVBK:nth-child(n+2){margin-left:0}.h99z3Q8GmSIKNBOeeAiG .HlWbgLppOhZms_A9w6Z0:empty{display:none}.h99z3Q8GmSIKNBOeeAiG .GPYRmffxeDTiFyipo8zb li{display:list-item;margin-left:20px}.h99z3Q8GmSIKNBOeeAiG .h_EtSEp1lTCy9STIZO5L{border-radius:3px;border-top-left-radius:0;border-top-right-radius:0;display:flex;overflow:hidden}.h99z3Q8GmSIKNBOeeAiG .h_EtSEp1lTCy9STIZO5L.dQuGau9j1Q3PRsbcQwXn{display:flex}.h99z3Q8GmSIKNBOeeAiG .h_EtSEp1lTCy9STIZO5L button.G2Ll9QfJcWmJebo2CLBK,.h99z3Q8GmSIKNBOeeAiG .h_EtSEp1lTCy9STIZO5L button.G3rXn0Z970cyYTTwHXGa,.h99z3Q8GmSIKNBOeeAiG .h_EtSEp1lTCy9STIZO5L button.r_2FW9iVF75rx81ukbjb,.h99z3Q8GmSIKNBOeeAiG .h_EtSEp1lTCy9STIZO5L button.Poy_zni69G1MJHTbBRBd,.h99z3Q8GmSIKNBOeeAiG .h_EtSEp1lTCy9STIZO5L button.QXsAnXbRz68nwQU_dgSg{background-color:#000;border:1px solid #333;border-radius:0;color:#fff;flex:1;font-weight:700;text-transform:uppercase;white-space:nowrap}.h99z3Q8GmSIKNBOeeAiG .h_EtSEp1lTCy9STIZO5L button.pJy4jv0wCbYmOztIGUJr,.h99z3Q8GmSIKNBOeeAiG .h_EtSEp1lTCy9STIZO5L.x3bDufLA6v9BXn_4STy8 button.QXsAnXbRz68nwQU_dgSg,.h99z3Q8GmSIKNBOeeAiG .h_EtSEp1lTCy9STIZO5L.YqEzCNfvcKKQzI76TyTL button.Poy_zni69G1MJHTbBRBd,.h99z3Q8GmSIKNBOeeAiG .N_NfcFJXan1SNkGllmjs,.pJy4jv0wCbYmOztIGUJr{display:none}@media only screen and (orientation:portrait){.SmCWLdwYU9nVmGKTxyLN,.XHuJMjwtrufVRq9lFsqA{display:none}}",
            ""
          ]), d.locals = {
            passport: "maifRQtxgpSscQm8oEQI",
            description: "SmCWLdwYU9nVmGKTxyLN",
            separator: "XHuJMjwtrufVRq9lFsqA",
            body: "h99z3Q8GmSIKNBOeeAiG",
            preview: "XTsf82b_Ippr6YQWXyFF",
            image: "KuLP9FswgqXlDXmRadny",
            webcam: "cOzCl1KRsY7md_B1rfty",
            overlay: "GPYRmffxeDTiFyipo8zb",
            gallery: "HlWbgLppOhZms_A9w6Z0",
            item: "MlrKTF6MEFsY5CbvCVBK",
            buttons: "h_EtSEp1lTCy9STIZO5L",
            both: "dQuGau9j1Q3PRsbcQwXn",
            add_btn: "G2Ll9QfJcWmJebo2CLBK",
            reset_btn: "G3rXn0Z970cyYTTwHXGa",
            retry_btn: "r_2FW9iVF75rx81ukbjb",
            take_btn: "Poy_zni69G1MJHTbBRBd",
            upload_btn: "QXsAnXbRz68nwQU_dgSg",
            hidden: "pJy4jv0wCbYmOztIGUJr",
            photo: "x3bDufLA6v9BXn_4STy8",
            scan: "YqEzCNfvcKKQzI76TyTL",
            file: "N_NfcFJXan1SNkGllmjs"
          };
          const p = d
        },
        3500: (e, t, r) => {
          r.d(t, {
            Z: () => f
          });
          var i = r(9601),
            n = r.n(i),
            o = r(2609),
            a = r.n(o),
            s = r(8991),
            c = r.n(s),
            l = new URL(r(8659), r.b),
            d = new URL(r(1566), r.b),
            u = new URL(r(8260), r.b),
            p = new URL(r(5494), r.b),
            v = a()(n()),
            m = c()(l),
            h = c()(d),
            g = c()(u),
            b = c()(p);
          v.push([e.id, ".xad3PZQLsj7YZa11mAag{--background:url(" + m +
            ");--background-color:#fff;--foreground-color:#000;--primary-color:#1ca1c1;--secondary-color:#ebedf0;--success-color:#27ae60;--warning-color:orange;--danger-color:#ff5c4c;--info-color:#a8a8a8;--preview-size:90px;--preview-border:4px;--preview-offset-x:10px;--preview-offset-y:10px;--dialog-close-btn:visible;all:initial;display:block;font-family:Arial,Helvetica,sans-serif;font-size:16px;height:0;left:0;line-height:1.5em;position:fixed;top:0;visibility:hidden;width:0;z-index:2147483647}.xad3PZQLsj7YZa11mAag ::-webkit-input-placeholder{-webkit-text-fill-color:initial;all:unset}.xad3PZQLsj7YZa11mAag *,.xad3PZQLsj7YZa11mAag ::placeholder,.xad3PZQLsj7YZa11mAag :after,.xad3PZQLsj7YZa11mAag :before{-webkit-text-fill-color:initial;all:unset}.xad3PZQLsj7YZa11mAag.M0__SL3fLgEbjW4usLRp{background-color:var(--secondary-color);background-image:url(" +
            h +
            ");background-position:50%;background-repeat:no-repeat;background-size:128px;bottom:0;height:100%;left:0;right:0;top:0;visibility:visible;width:100%}.xad3PZQLsj7YZa11mAag.M0__SL3fLgEbjW4usLRp iframe{visibility:hidden}.xad3PZQLsj7YZa11mAag video{background-color:#000;background-position:50%;background-repeat:no-repeat;background-size:contain;display:block;object-fit:contain}.xad3PZQLsj7YZa11mAag video[data-mirror]{transform:rotateY(180deg)}.xad3PZQLsj7YZa11mAag video[data-spinner]{background-image:url(" +
            g +
            ");background-size:auto;transform:none}.xad3PZQLsj7YZa11mAag video[data-off]{background-image:url(" +
            b +
            ");transform:none}.xad3PZQLsj7YZa11mAag a,.xad3PZQLsj7YZa11mAag a:active,.xad3PZQLsj7YZa11mAag a:focus,.xad3PZQLsj7YZa11mAag a:hover,.xad3PZQLsj7YZa11mAag a:visited{all:unset;color:var(--primary-color);cursor:pointer;display:inline;text-decoration:none}.xad3PZQLsj7YZa11mAag a:active{color:var(--danger-color)}.xad3PZQLsj7YZa11mAag a:hover{color:var(--primary-color)}.xad3PZQLsj7YZa11mAag button,.xad3PZQLsj7YZa11mAag button:active,.xad3PZQLsj7YZa11mAag button:disabled,.xad3PZQLsj7YZa11mAag button:focus,.xad3PZQLsj7YZa11mAag button:hover{all:unset;background-color:var(--primary-color);border-radius:3px;color:var(--background-color);cursor:default;display:inline;padding:8px;text-align:center}.xad3PZQLsj7YZa11mAag button:disabled{-webkit-filter:grayscale(1) brightness(.8);filter:grayscale(1) brightness(.8)}.xad3PZQLsj7YZa11mAag button:not(:disabled):hover{cursor:pointer;opacity:.8}.xad3PZQLsj7YZa11mAag input,.xad3PZQLsj7YZa11mAag input:active,.xad3PZQLsj7YZa11mAag input:disabled,.xad3PZQLsj7YZa11mAag input:focus,.xad3PZQLsj7YZa11mAag input:hover{all:unset;background-color:var(--secondary-color);border:none;border-bottom:2px solid var(--primary-color);border-radius:3px;box-sizing:border-box;display:inline-block;padding:8px;text-align:start}.xad3PZQLsj7YZa11mAag input:disabled{border-bottom-color:var(--info-color)}.xad3PZQLsj7YZa11mAag input::-webkit-input-placeholder{color:var(--info-color)}.xad3PZQLsj7YZa11mAag input::placeholder{color:var(--info-color)}.xad3PZQLsj7YZa11mAag textarea,.xad3PZQLsj7YZa11mAag textarea:active,.xad3PZQLsj7YZa11mAag textarea:disabled,.xad3PZQLsj7YZa11mAag textarea:focus,.xad3PZQLsj7YZa11mAag textarea:hover{all:unset;background-color:var(--background-color);border:1px solid var(--primary-color);border-radius:3px;box-sizing:border-box;cursor:text;display:inline-block;overflow-wrap:break-word;padding:4px 8px;resize:none;text-align:start;text-rendering:auto;white-space:pre-wrap}.xad3PZQLsj7YZa11mAag textarea::-webkit-input-placeholder{color:var(--info-color)}.xad3PZQLsj7YZa11mAag textarea::placeholder{color:var(--info-color)}",
            ""
          ]), v.locals = {
            proctoring: "xad3PZQLsj7YZa11mAag",
            modal: "M0__SL3fLgEbjW4usLRp"
          };
          const f = v
        },
        8497: (e, t, r) => {
          r.d(t, {
            Z: () => s
          });
          var i = r(9601),
            n = r.n(i),
            o = r(2609),
            a = r.n(o)()(n());
          a.push([e.id,
            ".OuyjZJLbkU4RWQDCV2W8{display:flex;height:100%}.YXDyKMFPebAB99GPmaln{padding:20px;width:40%}.M3NzIHOMxmmy1QZAnR3i{border-left:1px solid var(--secondary-color);margin:20px 0}.ksW0tUBc_4QHDVWCwB85{display:flex;flex:1;flex-direction:column;padding:20px}.OSva7x59meYDCeToaP8v,.MUXJxG_sDy21iAgnrrVV,.AZ2YDEvD4Grk08zocQYp{display:block}.MUXJxG_sDy21iAgnrrVV{display:flex;flex-direction:column;padding-bottom:8px}.OSva7x59meYDCeToaP8v{color:var(--info-color)}.OSva7x59meYDCeToaP8v sup{color:var(--danger-color)}.MUXJxG_sDy21iAgnrrVV .AZ2YDEvD4Grk08zocQYp{flex:1}.xHvs9NXQ5MWjBZRWet5V{background-color:var(--danger-color);border-radius:3px;display:block;padding:8px}.xHvs9NXQ5MWjBZRWet5V:empty{display:none}.xHvs9NXQ5MWjBZRWet5V .YMqO6oWL0Iagah8dEMug{color:var(--background-color);display:inline}@media only screen and (orientation:portrait){.YXDyKMFPebAB99GPmaln,.M3NzIHOMxmmy1QZAnR3i{display:none}}",
            ""
          ]), a.locals = {
            profile: "OuyjZJLbkU4RWQDCV2W8",
            description: "YXDyKMFPebAB99GPmaln",
            separator: "M3NzIHOMxmmy1QZAnR3i",
            body: "ksW0tUBc_4QHDVWCwB85",
            label: "OSva7x59meYDCeToaP8v",
            row: "MUXJxG_sDy21iAgnrrVV",
            value: "AZ2YDEvD4Grk08zocQYp",
            message: "xHvs9NXQ5MWjBZRWet5V",
            text: "YMqO6oWL0Iagah8dEMug"
          };
          const s = a
        },
        1059: (e, t, r) => {
          r.d(t, {
            Z: () => s
          });
          var i = r(9601),
            n = r.n(i),
            o = r(2609),
            a = r.n(o)()(n());
          a.push([e.id,
            ".zUeiJA2zB1xsBkzPSaxW{display:flex;height:100%}.M_m_Ca2QfF2kQuBoPx7V{padding:20px;width:40%}.mXZjWvuGnSu7FcwQq4Y2{border-left:1px solid var(--secondary-color);margin:20px 0}.jl0NHWJMCfXX0zG6Q4dR{display:flex;flex:1;padding:20px}.jl0NHWJMCfXX0zG6Q4dR .pzP9L6JCLkml4wyAbQPn{border:none;margin:auto;max-height:100%;max-width:100%;object-fit:contain}@media only screen and (orientation:portrait){.M_m_Ca2QfF2kQuBoPx7V,.mXZjWvuGnSu7FcwQq4Y2{display:none}}",
            ""
          ]), a.locals = {
            qrcode: "zUeiJA2zB1xsBkzPSaxW",
            description: "M_m_Ca2QfF2kQuBoPx7V",
            separator: "mXZjWvuGnSu7FcwQq4Y2",
            body: "jl0NHWJMCfXX0zG6Q4dR",
            img: "pzP9L6JCLkml4wyAbQPn"
          };
          const s = a
        },
        6605: (e, t, r) => {
          r.d(t, {
            Z: () => s
          });
          var i = r(9601),
            n = r.n(i),
            o = r(2609),
            a = r.n(o)()(n());
          a.push([e.id,
            ".gdLRFkGc_2OCnalRmspQ{display:flex;height:100%}.if17guSK0LtW_2xXLSb5{padding:20px;width:40%}.Jy_IL1N0gBd64bZdviBj{border-left:1px solid var(--secondary-color);margin:20px 0}.tb_LWk2GQfdCvD99dF7D{display:flex;flex:1;flex-direction:column;padding:20px}.ZjyaGySFeut8UbN815eC,.V8anJKEx9xYOoPGFmPZN,._nEMLMoujkZhxEEqSZ_g{display:block}.V8anJKEx9xYOoPGFmPZN{padding-bottom:8px}.ZjyaGySFeut8UbN815eC{color:var(--info-color)}.AdswdzRE5Eaz4Z5qPJSD{background-color:var(--danger-color);border-radius:3px;color:var(--background-color);margin-top:10px;padding:4px 8px}.AdswdzRE5Eaz4Z5qPJSD:empty,.FjpNhnZjg2zXpHcC8KgX{display:none}@media only screen and (orientation:portrait){.if17guSK0LtW_2xXLSb5,.Jy_IL1N0gBd64bZdviBj{display:none}}",
            ""
          ]), a.locals = {
            ready: "gdLRFkGc_2OCnalRmspQ",
            description: "if17guSK0LtW_2xXLSb5",
            separator: "Jy_IL1N0gBd64bZdviBj",
            body: "tb_LWk2GQfdCvD99dF7D",
            label: "ZjyaGySFeut8UbN815eC",
            row: "V8anJKEx9xYOoPGFmPZN",
            value: "_nEMLMoujkZhxEEqSZ_g",
            error: "AdswdzRE5Eaz4Z5qPJSD",
            hidden: "FjpNhnZjg2zXpHcC8KgX"
          };
          const s = a
        },
        6259: (e, t, r) => {
          r.d(t, {
            Z: () => s
          });
          var i = r(9601),
            n = r.n(i),
            o = r(2609),
            a = r.n(o)()(n());
          a.push([e.id,
            '.c8wB3YeG3t39AEgLzKql{display:flex;flex-direction:column;height:100%;overflow:hidden;padding:10px}.Z0GoCQtlj68YONFsnkjQ{-webkit-overflow-scrolling:touch;display:flex;flex:1;overflow-y:auto}.Z0GoCQtlj68YONFsnkjQ iframe{border:none;flex:1;overflow:auto}.Z0GoCQtlj68YONFsnkjQ iframe[src=""]{background:repeating-linear-gradient(45deg,#eee,#eee 15px,#fff 0,#fff 30px)}',
            ""
          ]), a.locals = {
            rules: "c8wB3YeG3t39AEgLzKql",
            iframe: "Z0GoCQtlj68YONFsnkjQ"
          };
          const s = a
        },
        1918: (e, t, r) => {
          r.d(t, {
            Z: () => s
          });
          var i = r(9601),
            n = r.n(i),
            o = r(2609),
            a = r.n(o)()(n());
          a.push([e.id,
            ".fuJszCgN0Qj6reiTleuf{display:flex;height:100%}.fyJAVnB9bXPHMkJgyZTE{padding:20px;width:40%}.UxdO3VtOKB6tOPo6Vi_3{border-left:1px solid var(--secondary-color);margin:20px 0}.B6lpBvWbD1puciy80IY9{display:flex;flex:1;flex-direction:column;padding:20px}.JnRaP7WJ_1PgE9kPUCUg,.a1OsvCDaCr1uYoEMrSk7,.tS4vIojzP16iVMRly3FG{display:block}.a1OsvCDaCr1uYoEMrSk7{display:flex;flex-direction:column;padding-bottom:8px}.JnRaP7WJ_1PgE9kPUCUg{color:var(--info-color)}.JnRaP7WJ_1PgE9kPUCUg sup{color:var(--danger-color)}.xXiPRlDVUOyRYyPn_L_N{background-color:var(--danger-color);border-radius:3px;display:block;padding:8px}.xXiPRlDVUOyRYyPn_L_N:empty{display:none}.xXiPRlDVUOyRYyPn_L_N .j3QT9nfYDzfJ3A3bx8Ug{color:var(--background-color);display:inline}.NIif99PNKz_GOwVqil6Z{display:none}.vRXN26LxNBf4HlUIP_dc{display:inline-block}@media only screen and (orientation:portrait){.fyJAVnB9bXPHMkJgyZTE,.UxdO3VtOKB6tOPo6Vi_3{display:none}}",
            ""
          ]), a.locals = {
            signup: "fuJszCgN0Qj6reiTleuf",
            description: "fyJAVnB9bXPHMkJgyZTE",
            separator: "UxdO3VtOKB6tOPo6Vi_3",
            body: "B6lpBvWbD1puciy80IY9",
            label: "JnRaP7WJ_1PgE9kPUCUg",
            row: "a1OsvCDaCr1uYoEMrSk7",
            value: "tS4vIojzP16iVMRly3FG",
            message: "xXiPRlDVUOyRYyPn_L_N",
            text: "j3QT9nfYDzfJ3A3bx8Ug",
            hidden: "NIif99PNKz_GOwVqil6Z",
            password: "vRXN26LxNBf4HlUIP_dc"
          };
          const s = a
        },
        6141: (e, t, r) => {
          r.d(t, {
            Z: () => M
          });
          var i = r(9601),
            n = r.n(i),
            o = r(2609),
            a = r.n(o),
            s = r(8991),
            c = r.n(s),
            l = new URL(r(4400), r.b),
            d = new URL(r(7922), r.b),
            u = new URL(r(2675), r.b),
            p = new URL(r(6302), r.b),
            v = new URL(r(1647), r.b),
            m = a()(n()),
            h = c()(l),
            g = c()(d),
            b = c()(u),
            f = c()(p),
            y = c()(v);
          m.push([e.id,
            '.JIfv7YI_yOSKzUPPUA4b{align-items:center;background-color:var(--background-color);bottom:var(--preview-offset-y);cursor:pointer;display:flex;height:var(--preview-size);left:var(--preview-offset-x);position:fixed;visibility:visible;width:var(--preview-size);will-change:transform;z-index:1}.r5iCms6jiL0q5vcxJqu0,.JIfv7YI_yOSKzUPPUA4b{border-radius:50%}.r5iCms6jiL0q5vcxJqu0{background:var(--info-color);bottom:calc(var(--preview-border)*-1);box-shadow:0 0 3px 0 rgba(0,0,0,.5);left:calc(var(--preview-border)*-1);right:calc(var(--preview-border)*-1);top:calc(var(--preview-border)*-1)}.r5iCms6jiL0q5vcxJqu0,.YaNorRUqXa3vWmeMiq0_{position:absolute}.YaNorRUqXa3vWmeMiq0_{bottom:10%;color:#fff;font-size:12px;font-weight:700;left:0;overflow:hidden;right:0;text-align:center;text-shadow:0 0 1px #000;z-index:1}.YaNorRUqXa3vWmeMiq0_:empty{display:none}.JIfv7YI_yOSKzUPPUA4b video{border-radius:50%;bottom:0;height:100%;left:0;object-fit:cover;overflow:hidden;position:absolute;right:0;top:0;width:100%}.NiVJjFvW0MlMxjyVTboW,.NiVJjFvW0MlMxjyVTboW+label{visibility:hidden}.NiVJjFvW0MlMxjyVTboW+label{background-color:rgba(0,0,0,.5);border-radius:50%;bottom:0;display:block;height:100%;left:0;overflow:hidden;position:absolute;right:0;top:0;width:100%;z-index:1}.JIfv7YI_yOSKzUPPUA4b .NiVJjFvW0MlMxjyVTboW:checked+label,.JIfv7YI_yOSKzUPPUA4b:hover .NiVJjFvW0MlMxjyVTboW+label{visibility:visible}.NiVJjFvW0MlMxjyVTboW+label:after,.NiVJjFvW0MlMxjyVTboW+label:before{background-color:var(--background-color);border-radius:4px;bottom:0;content:"";height:50%;left:0;margin:auto;position:absolute;right:0;top:0;transition:transform .25s;width:6px}.NiVJjFvW0MlMxjyVTboW+label:before{height:50%;width:6px}.NiVJjFvW0MlMxjyVTboW+label:after{height:6px;width:50%}.NiVJjFvW0MlMxjyVTboW:checked+label:after,.NiVJjFvW0MlMxjyVTboW:checked+label:before{transform:rotate(-45deg)}.ok3S9kBiyHuCN9eVzP01{bottom:0;display:flex;flex-flow:wrap-reverse;height:100%;left:0;position:absolute;right:0;top:0;transform:translateY(-100%);visibility:hidden;width:100%}.ok3S9kBiyHuCN9eVzP01 .slOjK6ylurAY3c7EcMyF{background-color:var(--background-color);border:2px solid var(--foreground-color);border-radius:50%;box-shadow:0 0 3px 0 rgba(0,0,0,.5);box-sizing:border-box;cursor:pointer;height:75%;margin:auto auto 5px;opacity:0;transition-duration:.1s;transition-property:opacity;width:75%}.ok3S9kBiyHuCN9eVzP01 .slOjK6ylurAY3c7EcMyF.T39BdHoZW6On3lLoOh3c{background:50%/60% var(--background-color) url(' +
            h +
            ") no-repeat}.ok3S9kBiyHuCN9eVzP01 .slOjK6ylurAY3c7EcMyF.mvhyw5w78QE9tcAL8vIg{background:50%/60% var(--background-color) url(" +
            g +
            ") no-repeat}.ok3S9kBiyHuCN9eVzP01 .slOjK6ylurAY3c7EcMyF.mCQfdAYOKKadJP6Kq2fX{background:50%/60% var(--background-color) url(" +
            b +
            ") no-repeat}.ok3S9kBiyHuCN9eVzP01 .slOjK6ylurAY3c7EcMyF.eJT3vFH99A8OrLqeTmqg{background:50%/60% var(--background-color) url(" +
            f +
            ') no-repeat}.tctRbr46eZIJu8385rey{background-color:var(--warning-color);border-radius:3px;box-shadow:0 0 3px 0 rgba(0,0,0,.5);color:var(--foreground-color);cursor:pointer;display:block;font-weight:700;line-height:1em;max-width:50vw;padding:10px;position:absolute;text-shadow:0 0 20px hsla(0,0%,100%,.5);top:50%;transform:perspective(1px) translateY(-50%);-webkit-user-select:none;-moz-user-select:none;user-select:none;visibility:visible;width:-moz-max-content;width:max-content}.yY_bbTL_9NrKxuKw17ME{left:115%}.vOFTl3Fq98K1JgqrHJya{right:115%}.yY_bbTL_9NrKxuKw17ME:after{border-color:transparent var(--warning-color) transparent transparent;border-style:solid;border-width:5px;content:" ";margin-top:-5px;position:absolute;right:100%;top:50%;visibility:visible}.yY_bbTL_9NrKxuKw17ME.ZgOrrsDeM66k_FODEx2m:after{border-color:transparent var(--danger-color) transparent transparent}.vOFTl3Fq98K1JgqrHJya:after{border-color:transparent transparent transparent var(--warning-color);border-style:solid;border-width:5px;content:" ";left:100%;margin-top:-5px;position:absolute;top:50%;visibility:visible}.vOFTl3Fq98K1JgqrHJya.ZgOrrsDeM66k_FODEx2m:after{border-color:transparent transparent transparent var(--danger-color)}.tctRbr46eZIJu8385rey.ZgOrrsDeM66k_FODEx2m{background-color:var(--danger-color)}.tctRbr46eZIJu8385rey .slOjK6ylurAY3c7EcMyF{background-color:initial;background-image:url(' +
            y +
            ");background-repeat:no-repeat;background-size:contain;display:inline-block;height:32px;padding:0;vertical-align:middle;visibility:visible;width:32px}.tctRbr46eZIJu8385rey .slOjK6ylurAY3c7EcMyF:hover{-webkit-filter:invert(.3);filter:invert(.3)}.NiVJjFvW0MlMxjyVTboW:checked~.ok3S9kBiyHuCN9eVzP01{visibility:visible}.NiVJjFvW0MlMxjyVTboW:checked~.ok3S9kBiyHuCN9eVzP01 .slOjK6ylurAY3c7EcMyF:first-child{margin-bottom:10px;opacity:1;transition-delay:.1s}.NiVJjFvW0MlMxjyVTboW:checked~.ok3S9kBiyHuCN9eVzP01 .slOjK6ylurAY3c7EcMyF:nth-child(2){opacity:1;transition-delay:.2s}.NiVJjFvW0MlMxjyVTboW:checked~.ok3S9kBiyHuCN9eVzP01 .slOjK6ylurAY3c7EcMyF:nth-child(3){opacity:1;transition-delay:.3s}.NiVJjFvW0MlMxjyVTboW:checked~.ok3S9kBiyHuCN9eVzP01 .slOjK6ylurAY3c7EcMyF:nth-child(4){opacity:1;transition-delay:.4s}.NiVJjFvW0MlMxjyVTboW:checked~.ok3S9kBiyHuCN9eVzP01 .slOjK6ylurAY3c7EcMyF:hover{border:2px solid var(--primary-color);transition-delay:0s}",
            ""
          ]), m.locals = {
            toolbar: "JIfv7YI_yOSKzUPPUA4b",
            border: "r5iCms6jiL0q5vcxJqu0",
            timer: "YaNorRUqXa3vWmeMiq0_",
            trigger: "NiVJjFvW0MlMxjyVTboW",
            tools: "ok3S9kBiyHuCN9eVzP01",
            btn: "slOjK6ylurAY3c7EcMyF",
            chat: "T39BdHoZW6On3lLoOh3c",
            calc: "mvhyw5w78QE9tcAL8vIg",
            qrcode: "mCQfdAYOKKadJP6Kq2fX",
            exit: "eJT3vFH99A8OrLqeTmqg",
            tooltip: "tctRbr46eZIJu8385rey",
            tooltip_right: "yY_bbTL_9NrKxuKw17ME",
            tooltip_left: "vOFTl3Fq98K1JgqrHJya",
            danger: "ZgOrrsDeM66k_FODEx2m"
          };
          const M = m
        },
        2609: e => {
          e.exports = function (e) {
            var t = [];
            return t.toString = function () {
              return this.map((function (t) {
                var r = "",
                  i = void 0 !== t[5];
                return t[4] && (r += "@supports (".concat(t[4], ") {")), t[2] && (r += "@media ".concat(
                  t[2], " {")), i && (r += "@layer".concat(t[5].length > 0 ? " ".concat(t[5]) : "",
                  " {")), r += e(t), i && (r += "}"), t[2] && (r += "}"), t[4] && (r += "}"), r
              })).join("")
            }, t.i = function (e, r, i, n, o) {
              "string" == typeof e && (e = [
                [null, e, void 0]
              ]);
              var a = {};
              if (i)
                for (var s = 0; s < this.length; s++) {
                  var c = this[s][0];
                  null != c && (a[c] = !0)
                }
              for (var l = 0; l < e.length; l++) {
                var d = [].concat(e[l]);
                i && a[d[0]] || (void 0 !== o && (void 0 === d[5] || (d[1] = "@layer".concat(d[5].length > 0 ?
                  " ".concat(d[5]) : "", " {").concat(d[1], "}")), d[5] = o), r && (d[2] ? (d[1] =
                  "@media ".concat(d[2], " {").concat(d[1], "}"), d[2] = r) : d[2] = r), n && (d[4] ? (d[
                    1] = "@supports (".concat(d[4], ") {").concat(d[1], "}"), d[4] = n) : d[4] = ""
                  .concat(n)), t.push(d))
              }
            }, t
          }
        },
        8991: e => {
          e.exports = function (e, t) {
            return t || (t = {}), e ? (e = String(e.__esModule ? e.default : e), /^['"].*['"]$/.test(e) && (e =
                e.slice(1, -1)), t.hash && (e += t.hash), /["'() \t\n]|(%20)/.test(e) || t.needQuotes ? '"'
              .concat(e.replace(/"/g, '\\"').replace(/\n/g, "\\n"), '"') : e) : e
          }
        },
        9601: e => {
          e.exports = function (e) {
            return e[1]
          }
        },
        2281: e => {
          const t = {
            generateIdentifier: function () {
              return Math.random().toString(36).substring(2, 12)
            }
          };
          t.localCName = t.generateIdentifier(), t.splitLines = function (e) {
            return e.trim().split("\n").map((e => e.trim()))
          }, t.splitSections = function (e) {
            return e.split("\nm=").map(((e, t) => (t > 0 ? "m=" + e : e).trim() + "\r\n"))
          }, t.getDescription = function (e) {
            const r = t.splitSections(e);
            return r && r[0]
          }, t.getMediaSections = function (e) {
            const r = t.splitSections(e);
            return r.shift(), r
          }, t.matchPrefix = function (e, r) {
            return t.splitLines(e).filter((e => 0 === e.indexOf(r)))
          }, t.parseCandidate = function (e) {
            let t;
            t = 0 === e.indexOf("a=candidate:") ? e.substring(12).split(" ") : e.substring(10).split(" ");
            const r = {
              foundation: t[0],
              component: {
                1: "rtp",
                2: "rtcp"
              } [t[1]] || t[1],
              protocol: t[2].toLowerCase(),
              priority: parseInt(t[3], 10),
              ip: t[4],
              address: t[4],
              port: parseInt(t[5], 10),
              type: t[7]
            };
            for (let e = 8; e < t.length; e += 2) switch (t[e]) {
            case "raddr":
              r.relatedAddress = t[e + 1];
              break;
            case "rport":
              r.relatedPort = parseInt(t[e + 1], 10);
              break;
            case "tcptype":
              r.tcpType = t[e + 1];
              break;
            case "ufrag":
              r.ufrag = t[e + 1], r.usernameFragment = t[e + 1];
              break;
            default:
              void 0 === r[t[e]] && (r[t[e]] = t[e + 1])
            }
            return r
          }, t.writeCandidate = function (e) {
            const t = [];
            t.push(e.foundation);
            const r = e.component;
            "rtp" === r ? t.push(1) : "rtcp" === r ? t.push(2) : t.push(r), t.push(e.protocol.toUpperCase()), t
              .push(e.priority), t.push(e.address || e.ip), t.push(e.port);
            const i = e.type;
            return t.push("typ"), t.push(i), "host" !== i && e.relatedAddress && e.relatedPort && (t.push(
                "raddr"), t.push(e.relatedAddress), t.push("rport"), t.push(e.relatedPort)), e.tcpType &&
              "tcp" === e.protocol.toLowerCase() && (t.push("tcptype"), t.push(e.tcpType)), (e
                .usernameFragment || e.ufrag) && (t.push("ufrag"), t.push(e.usernameFragment || e.ufrag)),
              "candidate:" + t.join(" ")
          }, t.parseIceOptions = function (e) {
            return e.substring(14).split(" ")
          }, t.parseRtpMap = function (e) {
            let t = e.substring(9).split(" ");
            const r = {
              payloadType: parseInt(t.shift(), 10)
            };
            return t = t[0].split("/"), r.name = t[0], r.clockRate = parseInt(t[1], 10), r.channels = 3 === t
              .length ? parseInt(t[2], 10) : 1, r.numChannels = r.channels, r
          }, t.writeRtpMap = function (e) {
            let t = e.payloadType;
            void 0 !== e.preferredPayloadType && (t = e.preferredPayloadType);
            const r = e.channels || e.numChannels || 1;
            return "a=rtpmap:" + t + " " + e.name + "/" + e.clockRate + (1 !== r ? "/" + r : "") + "\r\n"
          }, t.parseExtmap = function (e) {
            const t = e.substring(9).split(" ");
            return {
              id: parseInt(t[0], 10),
              direction: t[0].indexOf("/") > 0 ? t[0].split("/")[1] : "sendrecv",
              uri: t[1],
              attributes: t.slice(2).join(" ")
            }
          }, t.writeExtmap = function (e) {
            return "a=extmap:" + (e.id || e.preferredId) + (e.direction && "sendrecv" !== e.direction ? "/" + e
              .direction : "") + " " + e.uri + (e.attributes ? " " + e.attributes : "") + "\r\n"
          }, t.parseFmtp = function (e) {
            const t = {};
            let r;
            const i = e.substring(e.indexOf(" ") + 1).split(";");
            for (let e = 0; e < i.length; e++) r = i[e].trim().split("="), t[r[0].trim()] = r[1];
            return t
          }, t.writeFmtp = function (e) {
            let t = "",
              r = e.payloadType;
            if (void 0 !== e.preferredPayloadType && (r = e.preferredPayloadType), e.parameters && Object.keys(e
                .parameters).length) {
              const i = [];
              Object.keys(e.parameters).forEach((t => {
                void 0 !== e.parameters[t] ? i.push(t + "=" + e.parameters[t]) : i.push(t)
              })), t += "a=fmtp:" + r + " " + i.join(";") + "\r\n"
            }
            return t
          }, t.parseRtcpFb = function (e) {
            const t = e.substring(e.indexOf(" ") + 1).split(" ");
            return {
              type: t.shift(),
              parameter: t.join(" ")
            }
          }, t.writeRtcpFb = function (e) {
            let t = "",
              r = e.payloadType;
            return void 0 !== e.preferredPayloadType && (r = e.preferredPayloadType), e.rtcpFeedback && e
              .rtcpFeedback.length && e.rtcpFeedback.forEach((e => {
                t += "a=rtcp-fb:" + r + " " + e.type + (e.parameter && e.parameter.length ? " " + e
                  .parameter : "") + "\r\n"
              })), t
          }, t.parseSsrcMedia = function (e) {
            const t = e.indexOf(" "),
              r = {
                ssrc: parseInt(e.substring(7, t), 10)
              },
              i = e.indexOf(":", t);
            return i > -1 ? (r.attribute = e.substring(t + 1, i), r.value = e.substring(i + 1)) : r.attribute =
              e.substring(t + 1), r
          }, t.parseSsrcGroup = function (e) {
            const t = e.substring(13).split(" ");
            return {
              semantics: t.shift(),
              ssrcs: t.map((e => parseInt(e, 10)))
            }
          }, t.getMid = function (e) {
            const r = t.matchPrefix(e, "a=mid:")[0];
            if (r) return r.substring(6)
          }, t.parseFingerprint = function (e) {
            const t = e.substring(14).split(" ");
            return {
              algorithm: t[0].toLowerCase(),
              value: t[1].toUpperCase()
            }
          }, t.getDtlsParameters = function (e, r) {
            return {
              role: "auto",
              fingerprints: t.matchPrefix(e + r, "a=fingerprint:").map(t.parseFingerprint)
            }
          }, t.writeDtlsParameters = function (e, t) {
            let r = "a=setup:" + t + "\r\n";
            return e.fingerprints.forEach((e => {
              r += "a=fingerprint:" + e.algorithm + " " + e.value + "\r\n"
            })), r
          }, t.parseCryptoLine = function (e) {
            const t = e.substring(9).split(" ");
            return {
              tag: parseInt(t[0], 10),
              cryptoSuite: t[1],
              keyParams: t[2],
              sessionParams: t.slice(3)
            }
          }, t.writeCryptoLine = function (e) {
            return "a=crypto:" + e.tag + " " + e.cryptoSuite + " " + ("object" == typeof e.keyParams ? t
              .writeCryptoKeyParams(e.keyParams) : e.keyParams) + (e.sessionParams ? " " + e.sessionParams
              .join(" ") : "") + "\r\n"
          }, t.parseCryptoKeyParams = function (e) {
            if (0 !== e.indexOf("inline:")) return null;
            const t = e.substring(7).split("|");
            return {
              keyMethod: "inline",
              keySalt: t[0],
              lifeTime: t[1],
              mkiValue: t[2] ? t[2].split(":")[0] : void 0,
              mkiLength: t[2] ? t[2].split(":")[1] : void 0
            }
          }, t.writeCryptoKeyParams = function (e) {
            return e.keyMethod + ":" + e.keySalt + (e.lifeTime ? "|" + e.lifeTime : "") + (e.mkiValue && e
              .mkiLength ? "|" + e.mkiValue + ":" + e.mkiLength : "")
          }, t.getCryptoParameters = function (e, r) {
            return t.matchPrefix(e + r, "a=crypto:").map(t.parseCryptoLine)
          }, t.getIceParameters = function (e, r) {
            const i = t.matchPrefix(e + r, "a=ice-ufrag:")[0],
              n = t.matchPrefix(e + r, "a=ice-pwd:")[0];
            return i && n ? {
              usernameFragment: i.substring(12),
              password: n.substring(10)
            } : null
          }, t.writeIceParameters = function (e) {
            let t = "a=ice-ufrag:" + e.usernameFragment + "\r\na=ice-pwd:" + e.password + "\r\n";
            return e.iceLite && (t += "a=ice-lite\r\n"), t
          }, t.parseRtpParameters = function (e) {
            const r = {
                codecs: [],
                headerExtensions: [],
                fecMechanisms: [],
                rtcp: []
              },
              i = t.splitLines(e)[0].split(" ");
            r.profile = i[2];
            for (let n = 3; n < i.length; n++) {
              const o = i[n],
                a = t.matchPrefix(e, "a=rtpmap:" + o + " ")[0];
              if (a) {
                const i = t.parseRtpMap(a),
                  n = t.matchPrefix(e, "a=fmtp:" + o + " ");
                switch (i.parameters = n.length ? t.parseFmtp(n[0]) : {}, i.rtcpFeedback = t.matchPrefix(e,
                    "a=rtcp-fb:" + o + " ").map(t.parseRtcpFb), r.codecs.push(i), i.name.toUpperCase()) {
                case "RED":
                case "ULPFEC":
                  r.fecMechanisms.push(i.name.toUpperCase())
                }
              }
            }
            t.matchPrefix(e, "a=extmap:").forEach((e => {
              r.headerExtensions.push(t.parseExtmap(e))
            }));
            const n = t.matchPrefix(e, "a=rtcp-fb:* ").map(t.parseRtcpFb);
            return r.codecs.forEach((e => {
              n.forEach((t => {
                e.rtcpFeedback.find((e => e.type === t.type && e.parameter === t.parameter)) || e
                  .rtcpFeedback.push(t)
              }))
            })), r
          }, t.writeRtpDescription = function (e, r) {
            let i = "";
            i += "m=" + e + " ", i += r.codecs.length > 0 ? "9" : "0", i += " " + (r.profile ||
                "UDP/TLS/RTP/SAVPF") + " ", i += r.codecs.map((e => void 0 !== e.preferredPayloadType ? e
                .preferredPayloadType : e.payloadType)).join(" ") + "\r\n", i += "c=IN IP4 0.0.0.0\r\n", i +=
              "a=rtcp:9 IN IP4 0.0.0.0\r\n", r.codecs.forEach((e => {
                i += t.writeRtpMap(e), i += t.writeFmtp(e), i += t.writeRtcpFb(e)
              }));
            let n = 0;
            return r.codecs.forEach((e => {
              e.maxptime > n && (n = e.maxptime)
            })), n > 0 && (i += "a=maxptime:" + n + "\r\n"), r.headerExtensions && r.headerExtensions.forEach(
              (e => {
                i += t.writeExtmap(e)
              })), i
          }, t.parseRtpEncodingParameters = function (e) {
            const r = [],
              i = t.parseRtpParameters(e),
              n = -1 !== i.fecMechanisms.indexOf("RED"),
              o = -1 !== i.fecMechanisms.indexOf("ULPFEC"),
              a = t.matchPrefix(e, "a=ssrc:").map((e => t.parseSsrcMedia(e))).filter((e => "cname" === e
                .attribute)),
              s = a.length > 0 && a[0].ssrc;
            let c;
            const l = t.matchPrefix(e, "a=ssrc-group:FID").map((e => e.substring(17).split(" ").map((e =>
              parseInt(e, 10)))));
            l.length > 0 && l[0].length > 1 && l[0][0] === s && (c = l[0][1]), i.codecs.forEach((e => {
              if ("RTX" === e.name.toUpperCase() && e.parameters.apt) {
                let t = {
                  ssrc: s,
                  codecPayloadType: parseInt(e.parameters.apt, 10)
                };
                s && c && (t.rtx = {
                  ssrc: c
                }), r.push(t), n && (t = JSON.parse(JSON.stringify(t)), t.fec = {
                  ssrc: s,
                  mechanism: o ? "red+ulpfec" : "red"
                }, r.push(t))
              }
            })), 0 === r.length && s && r.push({
              ssrc: s
            });
            let d = t.matchPrefix(e, "b=");
            return d.length && (d = 0 === d[0].indexOf("b=TIAS:") ? parseInt(d[0].substring(7), 10) : 0 === d[0]
              .indexOf("b=AS:") ? 1e3 * parseInt(d[0].substring(5), 10) * .95 - 16e3 : void 0, r.forEach((
              e => {
                e.maxBitrate = d
              }))), r
          }, t.parseRtcpParameters = function (e) {
            const r = {},
              i = t.matchPrefix(e, "a=ssrc:").map((e => t.parseSsrcMedia(e))).filter((e => "cname" === e
                .attribute))[0];
            i && (r.cname = i.value, r.ssrc = i.ssrc);
            const n = t.matchPrefix(e, "a=rtcp-rsize");
            r.reducedSize = n.length > 0, r.compound = 0 === n.length;
            const o = t.matchPrefix(e, "a=rtcp-mux");
            return r.mux = o.length > 0, r
          }, t.writeRtcpParameters = function (e) {
            let t = "";
            return e.reducedSize && (t += "a=rtcp-rsize\r\n"), e.mux && (t += "a=rtcp-mux\r\n"), void 0 !== e
              .ssrc && e.cname && (t += "a=ssrc:" + e.ssrc + " cname:" + e.cname + "\r\n"), t
          }, t.parseMsid = function (e) {
            let r;
            const i = t.matchPrefix(e, "a=msid:");
            if (1 === i.length) return r = i[0].substring(7).split(" "), {
              stream: r[0],
              track: r[1]
            };
            const n = t.matchPrefix(e, "a=ssrc:").map((e => t.parseSsrcMedia(e))).filter((e => "msid" === e
              .attribute));
            return n.length > 0 ? (r = n[0].value.split(" "), {
              stream: r[0],
              track: r[1]
            }) : void 0
          }, t.parseSctpDescription = function (e) {
            const r = t.parseMLine(e),
              i = t.matchPrefix(e, "a=max-message-size:");
            let n;
            i.length > 0 && (n = parseInt(i[0].substring(19), 10)), isNaN(n) && (n = 65536);
            const o = t.matchPrefix(e, "a=sctp-port:");
            if (o.length > 0) return {
              port: parseInt(o[0].substring(12), 10),
              protocol: r.fmt,
              maxMessageSize: n
            };
            const a = t.matchPrefix(e, "a=sctpmap:");
            if (a.length > 0) {
              const e = a[0].substring(10).split(" ");
              return {
                port: parseInt(e[0], 10),
                protocol: e[1],
                maxMessageSize: n
              }
            }
          }, t.writeSctpDescription = function (e, t) {
            let r = [];
            return r = "DTLS/SCTP" !== e.protocol ? ["m=" + e.kind + " 9 " + e.protocol + " " + t.protocol +
                "\r\n", "c=IN IP4 0.0.0.0\r\n", "a=sctp-port:" + t.port + "\r\n"
              ] : ["m=" + e.kind + " 9 " + e.protocol + " " + t.port + "\r\n", "c=IN IP4 0.0.0.0\r\n",
                "a=sctpmap:" + t.port + " " + t.protocol + " 65535\r\n"
              ], void 0 !== t.maxMessageSize && r.push("a=max-message-size:" + t.maxMessageSize + "\r\n"), r
              .join("")
          }, t.generateSessionId = function () {
            return Math.random().toString().substr(2, 22)
          }, t.writeSessionBoilerplate = function (e, r, i) {
            let n;
            const o = void 0 !== r ? r : 2;
            n = e || t.generateSessionId();
            return "v=0\r\no=" + (i || "thisisadapterortc") + " " + n + " " + o +
              " IN IP4 127.0.0.1\r\ns=-\r\nt=0 0\r\n"
          }, t.getDirection = function (e, r) {
            const i = t.splitLines(e);
            for (let e = 0; e < i.length; e++) switch (i[e]) {
            case "a=sendrecv":
            case "a=sendonly":
            case "a=recvonly":
            case "a=inactive":
              return i[e].substring(2)
            }
            return r ? t.getDirection(r) : "sendrecv"
          }, t.getKind = function (e) {
            return t.splitLines(e)[0].split(" ")[0].substring(2)
          }, t.isRejected = function (e) {
            return "0" === e.split(" ", 2)[1]
          }, t.parseMLine = function (e) {
            const r = t.splitLines(e)[0].substring(2).split(" ");
            return {
              kind: r[0],
              port: parseInt(r[1], 10),
              protocol: r[2],
              fmt: r.slice(3).join(" ")
            }
          }, t.parseOLine = function (e) {
            const r = t.matchPrefix(e, "o=")[0].substring(2).split(" ");
            return {
              username: r[0],
              sessionId: r[1],
              sessionVersion: parseInt(r[2], 10),
              netType: r[3],
              addressType: r[4],
              address: r[5]
            }
          }, t.isValidSDP = function (e) {
            if ("string" != typeof e || 0 === e.length) return !1;
            const r = t.splitLines(e);
            for (let e = 0; e < r.length; e++)
              if (r[e].length < 2 || "=" !== r[e].charAt(1)) return !1;
            return !0
          }, e.exports = t
        },
        6062: e => {
          var t = [];
  
          function r(e) {
            for (var r = -1, i = 0; i < t.length; i++)
              if (t[i].identifier === e) {
                r = i;
                break
              } return r
          }
  
          function i(e, i) {
            for (var o = {}, a = [], s = 0; s < e.length; s++) {
              var c = e[s],
                l = i.base ? c[0] + i.base : c[0],
                d = o[l] || 0,
                u = "".concat(l, " ").concat(d);
              o[l] = d + 1;
              var p = r(u),
                v = {
                  css: c[1],
                  media: c[2],
                  sourceMap: c[3],
                  supports: c[4],
                  layer: c[5]
                };
              if (-1 !== p) t[p].references++, t[p].updater(v);
              else {
                var m = n(v, i);
                i.byIndex = s, t.splice(s, 0, {
                  identifier: u,
                  updater: m,
                  references: 1
                })
              }
              a.push(u)
            }
            return a
          }
  
          function n(e, t) {
            var r = t.domAPI(t);
            r.update(e);
            return function (t) {
              if (t) {
                if (t.css === e.css && t.media === e.media && t.sourceMap === e.sourceMap && t.supports === e
                  .supports && t.layer === e.layer) return;
                r.update(e = t)
              } else r.remove()
            }
          }
          e.exports = function (e, n) {
            var o = i(e = e || [], n = n || {});
            return function (e) {
              e = e || [];
              for (var a = 0; a < o.length; a++) {
                var s = r(o[a]);
                t[s].references--
              }
              for (var c = i(e, n), l = 0; l < o.length; l++) {
                var d = r(o[l]);
                0 === t[d].references && (t[d].updater(), t.splice(d, 1))
              }
              o = c
            }
          }
        },
        6793: e => {
          var t = {};
          e.exports = function (e, r) {
            var i = function (e) {
              if (void 0 === t[e]) {
                var r = document.querySelector(e);
                if (window.HTMLIFrameElement && r instanceof window.HTMLIFrameElement) try {
                  r = r.contentDocument.head
                } catch (e) {
                  r = null
                }
                t[e] = r
              }
              return t[e]
            }(e);
            if (!i) throw new Error(
              "Couldn't find a style target. This probably means that the value for the 'insert' parameter is invalid."
              );
            i.appendChild(r)
          }
        },
        1173: e => {
          e.exports = function (e) {
            var t = document.createElement("style");
            return e.setAttributes(t, e.attributes), e.insert(t, e.options), t
          }
        },
        7892: (e, t, r) => {
          e.exports = function (e) {
            var t = r.nc;
            t && e.setAttribute("nonce", t)
          }
        },
        4036: e => {
          e.exports = function (e) {
            if ("undefined" == typeof document) return {
              update: function () {},
              remove: function () {}
            };
            var t = e.insertStyleElement(e);
            return {
              update: function (r) {
                ! function (e, t, r) {
                  var i = "";
                  r.supports && (i += "@supports (".concat(r.supports, ") {")), r.media && (i += "@media "
                    .concat(r.media, " {"));
                  var n = void 0 !== r.layer;
                  n && (i += "@layer".concat(r.layer.length > 0 ? " ".concat(r.layer) : "", " {")), i += r
                    .css, n && (i += "}"), r.media && (i += "}"), r.supports && (i += "}");
                  var o = r.sourceMap;
                  o && "undefined" != typeof btoa && (i +=
                    "\n/*# sourceMappingURL=data:application/json;base64,".concat(btoa(unescape(
                      encodeURIComponent(JSON.stringify(o)))), " */")), t.styleTagTransform(i, e, t.options)
                }(t, e, r)
              },
              remove: function () {
                ! function (e) {
                  if (null === e.parentNode) return !1;
                  e.parentNode.removeChild(e)
                }(t)
              }
            }
          }
        },
        2464: e => {
          e.exports = function (e, t) {
            if (t.styleSheet) t.styleSheet.cssText = e;
            else {
              for (; t.firstChild;) t.removeChild(t.firstChild);
              t.appendChild(document.createTextNode(e))
            }
          }
        },
        8659: e => {
          e.exports =
            "data:image/png;base64,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"
        },
        7922: e => {
          e.exports =
            "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbDpzcGFjZT0icHJlc2VydmUiIHZpZXdCb3g9IjAgMCA0ODEuODgyIDQ4MS44ODIiIGZpbGw9IiMwMDAiPjxwYXRoIGQ9Ik0gMzkuMDIxNDg0LDQuMDA5NzY1NiBDIDI4LjUzNzQwMyw0LjEyNTYzMDQgMTguMjgzMjAxLDkuMjQ3MTY0NSAxMS43ODc1MTQsMTcuNDU5OTM3IGMgLTUuMjQzNTM5OCw2LjU0NTA2OSAtOC4wNTgyMDcxLDE0Ljk3MzQxIC03Ljc4NTYyMzgsMjMuMzU3MjUgOC43MjNlLTQsNDkuMzg4MjAyIC0wLjAxNTYxMyw5OC43NzY3MjMgMC4wMTc2NzIsMTQ4LjE2NDcyMyAwLjAxMTAzOCwxLjAwMjA4IDAuMTIxMzc2MywyLjI2NTExIDAuMjEwOTA2NiwzLjA5MDM2IDEuMTE0ODc5MSw5Ljc1NDI3IDYuNDcwNzU1MiwxOC45MjI1MyAxNC40MjIyNDQyLDI0LjY4MjQyIDYuMzU1OTg0LDQuNjY2IDE0LjI4MjIyMyw3LjEyODQzIDIyLjE2NDQ3NCw2Ljg3NjIzIDQ5LjM4ODIwMiwtOC43ZS00IDk4Ljc3NjcyMywwLjAxNTYgMTQ4LjE2NDcyMywtMC4wMTc3IDEuMDAyMDgsLTAuMDExIDIuMjY1MTEsLTAuMTIxMzggMy4wOTAzNiwtMC4yMTA5MSA5Ljc4Nzk5LC0xLjExNzQxIDE4Ljk4MzY4LC02LjUwODg4IDI0Ljc0MTc5LC0xNC41MDI3MSA0LjYyNzI0LC02LjM0NDQxIDcuMDYzNzIsLTE0LjIzODU2IDYuODE2ODYsLTIyLjA4NzkxIC05ZS00LC00OS4zODgyIDAuMDE1NywtOTguNzc2NzI2IC0wLjAxNzcsLTE0OC4xNjQ3MjQgLTAuMDE0NywtMS4wMzczOTggLTAuMTI1MTMsLTIuMzI5NzkyIC0wLjIyMzgyLC0zLjE4OTUxMyAtMS4xNDQwMiwtOS43NDkzMjIgLTYuNTIyNTEsLTE4LjkwMjI3NSAtMTQuNDkwMTIsLTI0LjYzODIzOCAtNi4zNDI4MiwtNC42Mjk3Njk2IC0xNC4yMzc5MSwtNy4wNjcxMTkzIC0yMi4wODc1NSwtNi44MTczNTQ4IC00OS4yNjM0MSwtMC4wMDU1OCAtOTguNTI2ODIzLC0wLjAwMjcgLTE0Ny43OTAyMzYsMC4wMDc4OCB6IG0gMjU0LjI0OTk5NiwwIGMgLTEwLjQ4NTE1LDAuMTE2MDk1IC0yMC43NDExMSw1LjIzNTczOTYgLTI3LjIzNzg3LDEzLjQ1MDE3MTQgLTUuMjQzMyw2LjU0NTI0IC04LjA1ODM4LDE0Ljk3MzI5MyAtNy43ODU2MywyMy4zNTcyNSA4LjhlLTQsNDkuMzg4MjAyIC0wLjAxNTYsOTguNzc2NzIzIDAuMDE3NywxNDguMTY0NzIzIDAuMDExLDEuMDAyMDggMC4xMjEzNywyLjI2NTExIDAuMjEwOSwzLjA5MDM2IDEuMTE0MzYsOS43NTU1OCA2LjQ3MjQ2LDE4LjkyMzQ2IDE0LjQyMzcxLDI0LjY4NTAzIDYuMzU3MDEsNC42NjUxOCAxNC4yODQ2Niw3LjEyNDc1IDIyLjE2NjkyLDYuODczNjIgNDkuMzg4MiwtOC43ZS00IDk4Ljc3NjcyLDAuMDE1NiAxNDguMTY0NzIsLTAuMDE3NyAxLjAwMjA4LC0wLjAxMSAyLjI2NTExLC0wLjEyMTM4IDMuMDkwMzYsLTAuMjEwOTEgOS40OTM2OCwtMS4wODY2OCAxOC40MzM2LC02LjE4NjI0IDI0LjIxMzExLC0xMy43OTQ2NiA0Ljk3MTA2LC02LjQ2NDU5IDcuNjAyNTksLTE0LjY2NDk2IDcuMzQ3NDYsLTIyLjgxNTEgLTAuMDAzLC00OS4zODE4MiAwLjAxMzQsLTk4Ljc2Mzk2NiAtMC4wMTk2LC0xNDguMTQ1NTg0IC0wLjAxMTQsLTEuMDAxOTc3IC0wLjEyNDc3LC0yLjI2NDk5MiAtMC4yMTI4MiwtMy4wOTAzNTUgLTEuMTE4NzUsLTkuNzg1NTc1IC02LjUwNjI0LC0xOC45ODIyODEgLTE0LjUwMTEyLC0yNC43MzczOTYgLTYuMzQyODIsLTQuNjI5NzY5NiAtMTQuMjM3OTEsLTcuMDY3MTE5MyAtMjIuMDg3NTUsLTYuODE3MzU0OCAtNDkuMjYzNDEsLTAuMDA1NTggLTk4LjUyNjgyLC0wLjAwMjcgLTE0Ny43OTAyNCwwLjAwNzg4IHogTSAxMDQuMjg3MTEsNDkuNzA3MDMxIGMgNy4wMTk1MywwIDE0LjAzOTA2LDAgMjEuMDU4NTksMCAwLDE3LjUyNjY5MyAwLDM1LjA1MzM4NiAwLDUyLjU4MDA3OSAxNy41MjczNSwwIDM1LjA1NDY5LDAgNTIuNTgyMDMsMCAwLDcuNjg2MiAwLDE1LjM3MjQgMCwyMy4wNTg1OSAtMTcuNTI3MzQsMCAtMzUuMDU0NjgsMCAtNTIuNTgyMDMsMCAwLDE3LjUyNzM1IDAsMzUuMDU0NjkgMCw1Mi41ODIwMyAtNy42ODY4NSwwIC0xNS4zNzM2OSwwIC0yMy4wNjA1NCwwIDAsLTE3LjUyNzM0IDAsLTM1LjA1NDY4IDAsLTUyLjU4MjAzIC0xNy41MjY2OTYsMCAtMzUuMDUzMzg5LDAgLTUyLjU4MDA4MiwwIDAsLTcuNjg2MTkgMCwtMTUuMzcyMzkgMCwtMjMuMDU4NTkgMTcuNTI3MzQ0LDAgMzUuMDU0Njg4LDAgNTIuNTgyMDMyLDAgMCwtMTcuNTI2NjkzIDAsLTM1LjA1MzM4NiAwLC01Mi41ODAwNzkgMC42NjY2NywwIDEuMzMzMzMsMCAyLDAgeiBtIDIwMS42NjQwNiw1Mi41ODAwNzkgYyA0Mi4wNzQyMiwwIDg0LjE0ODQ0LDAgMTI2LjIyMjY2LDAgMCw3LjY4NjIgMCwxNS4zNzI0IDAsMjMuMDU4NTkgLTQyLjc0MDg5LDAgLTg1LjQ4MTc3LDAgLTEyOC4yMjI2NiwwIDAsLTcuNjg2MTkgMCwtMTUuMzcyMzkgMCwtMjMuMDU4NTkgMC42NjY2NywwIDEuMzMzMzQsMCAyLDAgeiBNIDM5LjAyMTQ4NCwyNTguMjU1ODYgYyAtMTAuNDIxNTAxLDAuMTE3NTcgLTIwLjYyMDYzMSw1LjE3NTAxIC0yNy4xMTc5MTksMTMuMzA4NjcgLTUuMzIxMjIsNi41NjE0OCAtOC4xNzI0MzAzLDE1LjA1NDgyIC03LjkwMTY3NDgsMjMuNDk4NzUgOC43MjNlLTQsNDkuMzg5NTEgLTAuMDE1NjEzLDk4Ljc3OTMzIDAuMDE3NjcyLDE0OC4xNjg2MyAwLjAxMTAzOCwxLjAwMjA4IDAuMTIxMzc2MywyLjI2NTExIDAuMjEwOTA2NiwzLjA5MDM2IDEuMTE0ODc5MSw5Ljc1NDI3IDYuNDcwNzU1MiwxOC45MjI1MyAxNC40MjIyNDQyLDI0LjY4MjQyIDYuMzU2NDE2LDQuNjY1MjIgMTQuMjgyODIzLDcuMTI0NDggMjIuMTY0NDc0LDYuODc2MjMgNDkuMzg4MjAyLC04LjdlLTQgOTguNzc2NzIzLDAuMDE1NiAxNDguMTY0NzIzLC0wLjAxNzcgMTAuNTg0OSwtMC4yMzEyMyAyMC44ODc0NSwtNS41NTUxOSAyNy4yODIxMSwtMTMuOTgwMTMgNC45NzkyNywtNi40NjMxMyA3LjYyNzkyLC0xNC42NjU3OCA3LjM2NjksLTIyLjgyMTQgLTllLTQsLTQ5LjM4OTUgMC4wMTU3LC05OC43NzkzMyAtMC4wMTc3LC0xNDguMTY4NjMgLTAuMDE0NywtMS4wMzc0IC0wLjEyNTEzLC0yLjMyOTc5IC0wLjIyMzgyLC0zLjE4OTUxIC0xLjEzOTE0LC05LjcxNjYyIC02LjQ4NjA1LC0xOC44Mzk2IC0xNC40MDk2LC0yNC41Nzg5NCAtNi4zNTYxLC00LjY2ODYxIC0xNC4yODUyNiwtNy4xMjYxOSAtMjIuMTY4MDcsLTYuODc2NjYgLTQ5LjI2MzQxLC0wLjAwNiAtOTguNTI2ODIzLC0wLjAwMyAtMTQ3Ljc5MDIzNiwwLjAwOCB6IG0gMjU0LjI0OTk5NiwwIGMgLTEwLjQ1MTUsMC4xMTY0MyAtMjAuNjc3Niw1LjIwMDQ4IC0yNy4xNzQ2OSwxMy4zNzI2NiAtNS4yODQ0NCw2LjU1NDg4IC04LjEyMjQ3LDE1LjAxNzggLTcuODQ4ODEsMjMuNDM0NzYgOS4xZS00LDQ5LjM4OTUgLTAuMDE1Nyw5OC43NzkzMyAwLjAxNzcsMTQ4LjE2ODYzIDAuMjIzMTksMTAuMzE1ODIgNS4yODU1NSwyMC4zNjEyOSAxMy4zNDI0OCwyNi43ODU1OCA2LjU1OTQ2LDUuMjkxNDQgMTUuMDMwMDMsOC4xMzMzNCAyMy40NTQ3MSw3Ljg2NTM1IDQ5LjM4OTYzLC0wLjAwMyA5OC43Nzk1OSwwLjAxMzQgMTQ4LjE2OTAyLC0wLjAxOTYgMTAuMzU3NDcsLTAuMjI5MzEgMjAuNDQ2NDIsLTUuMzI4NjEgMjYuODY1MzQsLTEzLjQ0NjE5IDIuMzI0MTQsLTIuOTA5NDIgNC4xNzUyMiwtNi4xOTA3OCA1LjQ5NjUsLTkuNjcwOTMgMC4xMzYyNSwtMC4zODE3NyAwLjQxMTgzLC0xLjEyNjcxIDAuNTc2NzIsLTEuNjU1OTkgMS4zNTU1LC00LjA5MzgzIDEuODM4NDcsLTguNDI5MTcgMS43MTA0OSwtMTIuNzI4MzggLTguOWUtNCwtNDkuMTU2ODIgMC4wMTU2LC05OC4zMTM5NyAtMC4wMTc4LC0xNDcuNDcwNTggLTAuMDE0OSwtMS4wMzY2OCAtMC4xMjQ4NywtMi4zMjg2NiAtMC4yMjM3OSwtMy4xODc1NiAtMS4xMzk1LC05LjcxNzc2IC02LjQ4Nzc1LC0xOC44NDA1OSAtMTQuNDEwNzYsLTI0LjU4MTk3IC02LjM1ODQyLC00LjY2NjUzIC0xNC4yODcwNSwtNy4xMjMzOSAtMjIuMTcwODIsLTYuODc1NTUgLTQ5LjI2MjExLC0wLjAwNCAtOTguNTI0MjIsLTQuMmUtNCAtMTQ3Ljc4NjMzLDAuMDEgeiBtIDM5LjAyNTQsNTcuNzM4MjggYyAxMS45MjE4NywxMS45MjE4OCAyMy44NDM3NSwyMy44NDM3NSAzNS43NjU2MiwzNS43NjU2MyAxMi4zOTMyMywtMTIuMzkzMjMgMjQuNzg2NDYsLTI0Ljc4NjQ2IDM3LjE3OTY5LC0zNy4xNzk2OSA1LjQzNDY3LDUuNDM0NDcgMTAuODcwMDEsMTAuODY4MjYgMTYuMzA0NjksMTYuMzAyNzMgLTEyLjM5MzIzLDEyLjM5MzIzIC0yNC43ODY0NiwyNC43ODY0NiAtMzcuMTc5NjksMzcuMTc5NjkgMTIuMzkzMjMsMTIuMzkzMjMgMjQuNzg2NDYsMjQuNzg2NDYgMzcuMTc5NjksMzcuMTc5NjkgLTUuNDM0OSw1LjQzNDg5IC0xMC44Njk4LDEwLjg2OTc5IC0xNi4zMDQ2OSwxNi4zMDQ2OSAtMTIuMzkzMjMsLTEyLjM5MzIzIC0yNC43ODY0NiwtMjQuNzg2NDYgLTM3LjE3OTY5LC0zNy4xNzk2OSAtMTIuMzkzMjMsMTIuMzkzMjMgLTI0Ljc4NjQ2LDI0Ljc4NjQ2IC0zNy4xNzk2OSwzNy4xNzk2OSAtNS40MzQ0NywtNS40MzQ2OCAtMTAuODY4MjYsLTEwLjg3MDAyIC0xNi4zMDI3MywtMTYuMzA0NjkgMTIuMzkzMjMsLTEyLjM5MzIzIDI0Ljc4NjQ2LC0yNC43ODY0NiAzNy4xNzk2OSwtMzcuMTc5NjkgLTEyLjM5MzIzLC0xMi4zOTMyMyAtMjQuNzg2NDYsLTI0Ljc4NjQ2IC0zNy4xNzk2OSwtMzcuMTc5NjkgNS40MzQyNCwtNS40MzQyNCAxMC44Njg0OSwtMTAuODY4NDkgMTYuMzAyNzMsLTE2LjMwMjczIDAuNDcxMzYsMC40NzEzNSAwLjk0MjcxLDAuOTQyNzEgMS40MTQwNywxLjQxNDA2IHogTSA1MS43MDUwNzgsMzI2LjEwMzUyIGMgNDIuMDc0MjE5LDAgODQuMTQ4NDQyLDAgMTI2LjIyMjY1MiwwIDAsNy42ODYxOSAwLDE1LjM3MjM5IDAsMjMuMDU4NTkgLTQyLjc0MDg4LDAgLTg1LjQ4MTc2NiwwIC0xMjguMjIyNjUyLDAgMCwtNy42ODYyIDAsLTE1LjM3MjQgMCwtMjMuMDU4NTkgMC42NjY2NjcsMCAxLjMzMzMzMywwIDIsMCB6IG0gMCw2MC44NTc0MiBjIDQyLjA3NDIxOSwwIDg0LjE0ODQ0MiwwIDEyNi4yMjI2NTIsMCAwLDcuNjg2MiAwLDE1LjM3MjM5IDAsMjMuMDU4NTkgLTQyLjc0MDg4LDAgLTg1LjQ4MTc2NiwwIC0xMjguMjIyNjUyLDAgMCwtNy42ODYyIDAsLTE1LjM3MjM5IDAsLTIzLjA1ODU5IDAuNjY2NjY3LDAgMS4zMzMzMzMsMCAyLDAgeiIgLz48L3N2Zz4="
        },
        2158: e => {
          e.exports =
            "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbDpzcGFjZT0icHJlc2VydmUiIHZpZXdCb3g9IjAgMCA0ODQuNSA0ODQuNSIgZmlsbD0iI2ZmZiI+PHBhdGggZD0iTTQ4NC41LDExNC43NWwtMTAyLDEwMlYxMjcuNWMwLTE1LjMtMTAuMi0yNS41LTI1LjUtMjUuNUgxOTguOWwyODUuNiwyODUuNlYxMTQuNzV6IE0zMy4xNSwwTDAsMzMuMTVMNjguODUsMTAySDUxIGMtMTUuMywwLTI1LjUsMTAuMi0yNS41LDI1LjV2MjU1YzAsMTUuMywxMC4yLDI1LjUsMjUuNSwyNS41aDMwNmM1LjEsMCwxMC4yLTIuNTUsMTIuNzUtNS4xbDgxLjYsODEuNmwzMy4xNS0zMy4xNUwzMy4xNSwweiIvPjwvc3ZnPg=="
        },
        6712: e => {
          e.exports =
            "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbDpzcGFjZT0icHJlc2VydmUiIHZpZXdCb3g9IjAgMCA0NTkgNDU5IiBmaWxsPSIjZmZmIj48cGF0aCBkPSJNMzU3LDE5MS4yNVYxMDJjMC0xNS4zLTEwLjItMjUuNS0yNS41LTI1LjVoLTMwNkMxMC4yLDc2LjUsMCw4Ni43LDAsMTAydjI1NWMwLDE1LjMsMTAuMiwyNS41LDI1LjUsMjUuNWgzMDYgYzE1LjMsMCwyNS41LTEwLjIsMjUuNS0yNS41di04OS4yNWwxMDIsMTAyVjg5LjI1TDM1NywxOTEuMjV6Ii8+PC9zdmc+"
        },
        4400: e => {
          e.exports =
            "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbDpzcGFjZT0icHJlc2VydmUiIHZpZXdCb3g9IjAgMCA1MTIgNTEyIiBmaWxsPSIjMDAwIj48cGF0aCBkPSJNNDc0LjA2IDQ0SDEyMi43NGMtMjEuMDc5IDAtMzcuOTQyIDE3LjQzNi0zNy45NDIgMzguMTcxdjIxOS42YzAgMjEuMjA2IDE3LjMzMiAzOC4xNzEgMzcuOTQyIDM4LjE3MWgyNDIuMTdsNTQuODA1IDU1LjYwOGMyLjM0MiAyLjM1NiA1LjE1MyAzLjc3IDguNDMyIDMuNzcgNi41NTcgMCAxMi4xNzktNS4xODQgMTIuMTc5LTEyLjI1M3YtNDcuMTI1aDMzLjcyNmMyMS4wNzkgMCAzNy45NDItMTcuNDM2IDM3Ljk0Mi0zOC4xNzF2LTIxOS42YzAtMjEuMjA2LTE3LjMzMi0zOC4xNzEtMzcuOTQyLTM4LjE3MXpNMTc2LjYxIDIzMi45N2MtMTkuMjA1IDAtMzUuMTMyLTE2LjAyMy0zNS4xMzItMzUuMzQ0czE1LjkyNi0zNS4zNDQgMzUuMTMyLTM1LjM0NGMxOS4yMDUgMCAzNS4xMzIgMTYuMDIzIDM1LjEzMiAzNS4zNDRzLTE1LjQ1OCAzNS4zNDQtMzUuMTMyIDM1LjM0NHptMTIzLjIgMGMtMTkuMjA1IDAtMzUuMTMyLTE2LjAyMy0zNS4xMzItMzUuMzQ0czE1LjkyNi0zNS4zNDQgMzUuMTMyLTM1LjM0NGMxOS4yMDUgMCAzNS4xMzIgMTYuMDIzIDM1LjEzMiAzNS4zNDRzLTE1LjkyNiAzNS4zNDQtMzUuMTMyIDM1LjM0NHptMTIyLjczIDBjLTE5LjIwNSAwLTM1LjEzMi0xNi4wMjMtMzUuMTMyLTM1LjM0NHMxNS45MjYtMzUuMzQ0IDM1LjEzMi0zNS4zNDRjMTkuMjA1IDAgMzUuMTMyIDE2LjAyMyAzNS4xMzIgMzUuMzQ0cy0xNS45MjYgMzUuMzQ0LTM1LjEzMiAzNS4zNDR6Ii8+PHBhdGggZD0iTTYzLjI1MSAzMDIuNzJ2LTc0LjkyOUgyNC44NGMtMTMuNTg0IDAtMjQuODI2IDExLjMxLTI0LjgyNiAyNC45NzZ2MTQ0LjJjLS40NjggMTQuNjA5IDEwLjc3NCAyNS45MTkgMjQuODI2IDI1LjkxOWgyMi4wMTZ2MzEuMTAzYzAgNC4yNDEgMy43NDcgOC4wMTEgNy45NjMgOC4wMTEgMi4zNDIgMCA0LjIxNi0uOTQyIDUuNjIxLTIuMzU2bDM2LjA3LTM2LjI4NmgxNTkuMjZjMTMuNTgzIDAgMjQuODI1LTExLjMxIDI0LjgyNS0yNC45NzZ2LTM1LjgxNWgtMTU3Ljg2Yy0zMi43OSAwLTU5LjQ5LTI2Ljg2MS01OS40OS01OS44NDl6Ii8+PC9zdmc+Cg=="
        },
        7521: e => {
          e.exports =
            "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbDpzcGFjZT0icHJlc2VydmUiIHZpZXdCb3g9IjAgMCA1MTIgNTEyIiBmaWxsPSIjODA4MDgwIj48cGF0aCBkPSJtNDE5LjA3IDE1OS4wNGMtMTAuOTU5IDAtMjEuMDQxIDQuMzkwOC0yOC40OTMgMTEuODU1LTcuNDUyMSA3LjQ2NDMtMTEuODM2IDE3LjU2My0xMS44MzYgMjguNTRzNC4zODM2IDIxLjA3NiAxMS44MzYgMjguNTRjNy40NTIgNy4wMjUyIDE3LjUzNCAxMS44NTUgMjguNDkzIDExLjg1NXMyMS4wNDEtNC4zOTA4IDI4LjQ5My0xMS44NTVjNy40NTItNy40NjQzIDExLjgzNi0xNy41NjMgMTEuODM2LTI4LjU0cy00LjM4MzYtMjEuMDc2LTExLjgzNi0yOC41NGMtNy40NTIxLTcuNDY0My0xNy41MzQtMTEuODU1LTI4LjQ5My0xMS44NTV6bTIwLjE2NCA2MC41OTJjLTUuMjYwMyA1LjI2ODktMTIuMjc0IDguMzQyNC0yMC4xNjQgOC4zNDI0LTcuODkwNCAwLTE0LjkwNC0zLjA3MzUtMjAuMTY0LTguMzQyNC01LjI2MDMtNS4yNjg5LTguMzI4OC0xMi4yOTQtOC4zMjg4LTIwLjE5N3MzLjA2ODUtMTUuMzY4IDguMzI4OC0yMC4xOTdjNS4yNjAzLTUuMjY4OSAxMi4yNzQtOC4zNDI0IDIwLjE2NC04LjM0MjQgNy44OTA0IDAgMTQuOTA0IDMuMDczNSAyMC4xNjQgOC4zNDI0IDUuMjYwMyA1LjI2ODkgOC4zMjg4IDEyLjI5NCA4LjMyODggMjAuMTk3cy0zLjA2ODUgMTQuOTI5LTguMzI4OCAyMC4xOTd6Ii8+PHBhdGggZD0ibTE3OC44NSAxNTkuMDRjLTEwLjk1OSAwLTIxLjA0MSA0LjM5MDgtMjguNDkzIDExLjg1NS03LjQ1MiA3LjQ2NDMtMTEuODM2IDE3LjU2My0xMS44MzYgMjguNTRzNC4zODM2IDIxLjA3NiAxMS44MzYgMjguNTRjNy4wMTM3IDcuMDI1MiAxNy4wOTYgMTEuODU1IDI4LjQ5MyAxMS44NTUgMTAuOTU5IDAgMjEuMDQxLTQuMzkwOCAyOC40OTMtMTEuODU1IDcuNDUyLTcuNDY0MyAxMS44MzYtMTcuNTYzIDExLjgzNi0yOC41NHMtNC4zODM2LTIxLjA3Ni0xMS44MzYtMjguNTRjLTcuNDUyMS03LjQ2NDMtMTcuNTM0LTExLjg1NS0yOC40OTMtMTEuODU1em0yMC4xNjQgNjAuNTkyYy01LjI2MDMgNS4yNjg5LTEyLjI3NCA4LjM0MjQtMjAuMTY0IDguMzQyNC03Ljg5MDQgMC0xNC45MDQtMy4wNzM1LTIwLjE2NC04LjM0MjQtNS4yNjAzLTUuMjY4OS04LjMyODgtMTIuMjk0LTguMzI4OC0yMC4xOTdzMy4wNjg1LTE1LjM2OCA4LjMyODgtMjAuMTk3YzUuMjYwMy01LjI2ODkgMTIuMjc0LTguMzQyNCAyMC4xNjQtOC4zNDI0IDcuODkwNCAwIDE0LjkwNCAzLjA3MzUgMjAuMTY0IDguMzQyNCA1LjI2MDMgNS4yNjg5IDguMzI4OCAxMi4yOTQgOC4zMjg4IDIwLjE5N3MtMy4wNjg1IDE0LjkyOS04LjMyODggMjAuMTk3eiIvPjxwYXRoIGQ9Im0yOTguOTYgMTU5LjA0Yy0xMC45NTkgMC0yMS4wNDEgNC4zOTA4LTI4LjQ5MyAxMS44NTUtNy40NTIxIDcuNDY0My0xMS44MzYgMTcuNTYzLTExLjgzNiAyOC41NHM0LjM4MzYgMjEuMDc2IDExLjgzNiAyOC41NGM3LjAxMzcgNy4wMjUyIDE3LjA5NiAxMS44NTUgMjguNDkzIDExLjg1NSAxMC45NTkgMCAyMS4wNDEtNC4zOTA4IDI4LjQ5My0xMS44NTUgNy40NTIxLTcuNDY0MyAxMS44MzYtMTcuNTYzIDExLjgzNi0yOC41NHMtNC4zODM2LTIxLjA3Ni0xMS44MzYtMjguNTRjLTcuNDUyLTcuNDY0My0xNy41MzQtMTEuODU1LTI4LjQ5My0xMS44NTV6bTIwLjE2NCA2MC41OTJjLTUuMjYwMyA1LjI2ODktMTIuMjc0IDguMzQyNC0yMC4xNjQgOC4zNDI0LTcuODkwNCAwLTE0LjkwNC0zLjA3MzUtMjAuMTY0LTguMzQyNHMtOC4zMjg4LTEyLjI5NC04LjMyODgtMjAuMTk3IDMuMDY4NS0xNS4zNjggOC4zMjg4LTIwLjE5N2M1LjI2MDMtNS4yNjg5IDEyLjI3NC04LjM0MjQgMjAuMTY0LTguMzQyNCA3Ljg5MDQgMCAxNC45MDQgMy4wNzM1IDIwLjE2NCA4LjM0MjQgNS4yNjAzIDUuMjY4OSA4LjMyODggMTIuMjk0IDguMzI4OCAyMC4xOTdzLTMuMDY4NSAxNC45MjktOC4zMjg4IDIwLjE5N3oiLz48cGF0aCBkPSJtNDk5LjI5IDU2LjczM2MtNy44OTA0LTcuOTAzNC0xOC40MTEtMTIuNzMzLTMwLjI0Ny0xMi43MzNoLTM0My4yM2MtMTEuODM2IDAtMjIuNzk1IDQuODI5OC0zMC4yNDcgMTIuNzMzLTcuODkwNCA3LjkwMzQtMTIuNzEyIDE4LjQ0MS0xMi43MTIgMzAuMjk2djEzNi4xMWgtNTIuNjAzYy04LjMyODggMC0xNS43ODEgMy41MTI2LTIxLjQ3OSA4Ljc4MTUtNS42OTg2IDUuNzA4LTguNzY3MSAxMy4xNzItOC43NjcxIDIxLjUxNXYxNDAuNWMwIDguMzQyNCAzLjUwNjggMTUuODA3IDguNzY3MSAyMS41MTUgNS4yNjAzIDUuMjY4OSAxMi43MTIgOC43ODE1IDIxLjA0MSA4Ljc4MTVoMTUuNzgxdjI0LjE0OWMwIDMuOTUxNyAxLjMxNTEgNy4wMjUyIDMuOTQ1MiA5LjY1OTcgMi42MzAxIDIuNjM0NCA1LjY5ODYgMy45NTE3IDkuNjQzOCAzLjk1MTcgMS43NTM0IDAgMy41MDY4LTAuNDM5MDggNS4yNjAzLTAuODc4MTUgMS43NTM0LTAuODc4MTYgMy4wNjg1LTEuNzU2MyA0LjM4MzYtMy4wNzM1bDMzLjc1My0zMy44MDloMTUzLjQyYzguMzI4OCAwIDE1Ljc4MS0zLjUxMjYgMjEuNDc5LTguNzgxNSA1LjY5ODYtNS43MDggOC43NjcxLTEzLjE3MiA4Ljc2NzEtMjEuNTE1di01MC4wNTVoNzMuNjQ0bDUyLjE2NCA1Mi4yNWMxLjc1MzQgMS43NTYzIDMuNTA2OCAzLjA3MzUgNS42OTg2IDMuOTUxNyAyLjE5MTggMC44NzgxNiA0LjM4MzYgMS4zMTcyIDYuNTc1NCAxLjMxNzIgNC44MjE5IDAgOS4yMDU1LTEuNzU2MyAxMi4yNzQtNS4yNjg5IDMuMDY4NS0zLjA3MzUgNS4yNjAzLTcuNDY0MyA1LjI2MDMtMTIuMjk0di0zOS45NTZoMjcuMTc4YzExLjgzNiAwIDIyLjc5NS00LjgyOTggMzAuMjQ3LTEyLjczMyA3Ljg5MDQtNy45MDM0IDEyLjcxMi0xOC40NDEgMTIuNzEyLTMwLjI5NnYtMjEzLjgzYzAtMTEuODU1LTQuODIxOS0yMi44MzItMTIuNzEyLTMwLjI5NnptLTIyNS4zMiAzMzcuMjFjMCA1LjI2ODktMi4xOTE4IDkuNjU5Ny01LjI2MDMgMTMuMTcyLTMuNTA2OCAzLjUxMjYtNy44OTA0IDUuMjY4OS0xMy4xNTEgNS4yNjg5aC0xNTUuMThjLTEuMzE1MSAwLTMuMDY4NSAwLjQzOTA4LTMuOTQ1MiAxLjc1NjNsLTM1Ljk0NSAzNi4wMDRoLTAuODc2NzFjLTAuNDM4MzYgMC0wLjg3NjcxIDAtMS4zMTUxLTAuNDM5MDgtMC40MzgzNi0wLjQzOTA3LTAuNDM4MzYtMC44NzgxNS0wLjQzODM2LTEuMzE3MnYtMzAuMjk2YzAtMy4wNzM1LTIuNjMwMS01LjcwOC01LjY5ODYtNS43MDhoLTIxLjQ3OWMtNS4yNjAzIDAtOS42NDM4LTIuMTk1NC0xMy4xNTEtNS4yNjg5LTMuNTA2OC0zLjUxMjYtNS4yNjAzLTcuOTAzNC01LjI2MDMtMTMuMTcydi0xNDAuNWgtMC44NzY3MWMwLTUuMjY4OSAyLjE5MTgtOS42NTk3IDUuMjYwMy0xMy4xNzIgMy41MDY4LTMuNTEyNiA3Ljg5MDQtNS4yNjg5IDEzLjE1MS01LjI2ODloNTIuNjAzdjY1Ljg2MWMwIDExLjg1NSA0LjgyMTkgMjIuODMyIDEyLjcxMiAzMC4yOTYgNy44OTA0IDcuOTAzNCAxOC40MTEgMTIuNzMzIDMwLjI0NyAxMi43MzNoMTQ4LjZ6bTIyNy4wNy05My4wODRjMCA4Ljc4MTUtMy41MDY4IDE2LjY4NS05LjIwNTUgMjIuMzkzLTUuNjk4NiA1LjcwOC0xMy41ODkgOS4yMjA2LTIyLjM1NiA5LjIyMDZoLTMyLjg3N2MtMy4wNjg1IDAtNS42OTg2IDIuNjM0NS01LjY5ODYgNS43MDh2NDUuNjY0YzAgMS43NTYzLTAuNDM4MzUgMy4wNzM1LTEuNzUzNCAzLjk1MTctMC44NzY3MiAwLjg3ODE1LTIuNjMwMSAxLjc1NjMtMy45NDUyIDEuNzU2My0wLjg3NjcxIDAtMS43NTM0IDAtMi4xOTE4LTAuNDM5MDctMC44NzY3MS0wLjQzOTA4LTEuMzE1MS0wLjg3ODE2LTEuNzUzNC0xLjMxNzJsLTU0Ljc5NS01NC4wMDZjLTEuMzE1MS0xLjMxNzItMi42MzAxLTEuNzU2My0zLjk0NTItMS43NTYzaC0yMzYuNzFjLTguNzY3MSAwLTE2LjY1OC0zLjUxMjYtMjIuMzU2LTkuMjIwNi01LjY5ODYtNS43MDgtOS4yMDU1LTEzLjYxMS05LjIwNTUtMjIuMzkzdi0yMTMuMzljMC04Ljc4MTUgMy41MDY4LTE2LjY4NSA5LjIwNTUtMjIuMzkzIDUuNjk4Ni01LjcwOCAxMy41ODktOS4yMjA2IDIyLjM1Ni05LjIyMDZoMzQzLjY3YzguNzY3MSAwIDE2LjY1OCAzLjUxMjYgMjIuMzU2IDkuMjIwNiA1LjY5ODYgNS43MDggOS4yMDU1IDEzLjYxMSA5LjIwNTUgMjIuMzkzeiIvPjwvc3ZnPg=="
        },
        6323: e => {
          e.exports =
            "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbDpzcGFjZT0icHJlc2VydmUiIHZpZXdCb3g9IjAgMCA1MTIgNTEyIiBmaWxsPSIjODA4MDgwIj48ZyB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtMTEuOSA2LjQpIj48cGF0aCBkPSJtMjQ5Ljc3IDIyMS45NmM2Ljk4OTUtNy4wNDY5IDYuOTg5NS0xOC40OTggMC0yNS41NDUtNi45ODk2LTcuMDQ2OS0xOC4zNDgtNy4wNDY5LTI1LjMzNyAwbC05NC43OTYgOTUuNTczYy0xNi4xNjMgMTYuMjk2LTI0LjkgMzcuNDM3LTI0LjkgNjAuMzM5czguNzM3IDQ0LjA0MyAyNC45IDYwLjMzOWMzMy4yIDMzLjQ3MyA4Ni45MzMgMzMuNDczIDExOS43IDBsMjE0LjA2LTIxNS44MWMyMi4yNzktMjIuNDYyIDM0LjUxMS01Mi40MTEgMzQuNTExLTg0LjEyMnMtMTIuMjMyLTYxLjY2LTM0LjUxMS04NC4xMjJjLTQ2LjMwNi00Ni42ODYtMTIxLjAxLTQ2LjY4Ni0xNjcuMzEgMGwtMjEzLjYyIDIxNS4zN2MtMjguODMyIDI5LjA2OC00NC41NTggNjcuMzg2LTQ0LjU1OCAxMDguMzUgMCA0MC45NiAxNS43MjYgNzkuNzE4IDQ0LjU1OCAxMDguMzUgMjguODMyIDI5LjA2OCA2Ni44MzggNDQuOTI0IDEwNy40NiA0NC45MjRzNzkuMDY5LTE1Ljg1NSAxMDcuNDYtNDQuOTI0bDk0Ljc5Ni05NS41NzNjNi45ODk2LTcuMDQ2OSA2Ljk4OTYtMTguNDk4IDAtMjUuNTQ1LTYuOTg5NS03LjA0NjktMTguMzQ4LTcuMDQ2OS0yNS4zMzcgMGwtOTQuNzk2IDk1LjU3M2MtMjEuODQyIDIyLjAyMi01MS4xMTEgMzQuMzU0LTgyLjEyNyAzNC4zNTRzLTYwLjI4NS0xMi4zMzItODIuMTI3LTM0LjM1NGMtMjEuODQyLTIyLjAyMS0zNC4wNzQtNTEuNTMtMzQuMDc0LTgyLjgwMXMxMi4yMzItNjAuNzc5IDM0LjA3NC04Mi44MDFsMjEzLjYyLTIxNS4zN2MxNS43MjYtMTUuODU1IDM2LjI1OC0yNC4yMjQgNTguMTAxLTI0LjIyNCAyMS44NDIgMCA0Mi44MTEgOC44MDg2IDU4LjEwMSAyNC4yMjQgMTUuNzI2IDE1Ljg1NSAyNC4wMjcgMzYuNTU2IDI0LjAyNyA1OC41NzdzLTguNzM2OSA0My4xNjItMjQuMDI3IDU4LjU3N2wtMjE0LjA2IDIxNS44MWMtMTguNzg0IDE4LjkzOC00OS44MDEgMTguOTM4LTY5LjAyMiAwLTkuMTczOC05LjI0OTEtMTQuNDE2LTIxLjU4MS0xNC40MTYtMzQuNzk0czUuMjQyMi0yNS41NDUgMTQuNDE2LTM0Ljc5NHoiIHN0cm9rZS13aWR0aD0iNC4zODYzIi8+PC9nPjwvc3ZnPg=="
        },
        8632: e => {
          e.exports =
            "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbDpzcGFjZT0icHJlc2VydmUiIHZpZXdCb3g9IjAgMCA1MTIgNTEyIiBmaWxsPSIjODA4MDgwIj48cGF0aCBkPSJtMzAxLjI4IDI1Ni4wMSAyMDEuMzQtMjAxLjM1YzEyLjUwOS0xMi40OTkgMTIuNTA5LTMyLjc3OSAwLTQ1LjI3Ny0xMi41MDktMTIuNTA5LTMyLjc2Ni0xMi41MDktNDUuMjc1IDBsLTIwMS4zNCAyMDEuMzUtMjAxLjM1LTIwMS4zNWMtMTIuNTA5LTEyLjUwOS0zMi43NjYtMTIuNTA5LTQ1LjI3NSAwLTEyLjUwOSAxMi40OTktMTIuNTA5IDMyLjc3OSAwIDQ1LjI3N2wyMDEuMzUgMjAxLjM1LTIwMS4zNSAyMDEuMzVjLTEyLjUwOSAxMi40OTktMTIuNTA5IDMyLjc3OSAwIDQ1LjI3NyA2LjI1NDQgNi4yNDQgMTQuNDUxIDkuMzcxNCAyMi42MzggOS4zNzE0czE2LjM4My0zLjEyNzQgMjIuNjM4LTkuMzgyMWwyMDEuMzUtMjAxLjM1IDIwMS4zNCAyMDEuMzVjNi4yNTQ0IDYuMjU0NyAxNC40NTEgOS4zODIxIDIyLjYzOCA5LjM4MjEgOC4xODYzIDAgMTYuMzgzLTMuMTI3NCAyMi42MzgtOS4zODIxIDEyLjUwOS0xMi40OTkgMTIuNTA5LTMyLjc3OCAwLTQ1LjI3N3oiIHN0cm9rZS13aWR0aD0iMTAuNjczIi8+PC9zdmc+"
        },
        6302: e => {
          e.exports =
            "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbDpzcGFjZT0icHJlc2VydmUiIHZpZXdCb3g9IjAgMCAzMiAzMiIgZmlsbD0iIzAwMCI+PHBhdGggZD0ibTMxLjEgMTQuN2MtMC4xLTAuMS0wLjEtMC4yLTAuMi0wLjNsLTQtNGMtMC40LTAuNC0xLTAuNC0xLjQgMHMtMC40IDEgMCAxLjRsMi4zIDIuM2gtNS42di0xMGMwLTAuNi0wLjQtMS0xLTFoLTE3Yy0wLjEgMC0wLjMgMC0wLjQgMC4xaC0wLjFzLTAuMSAwLTAuMSAwLjFsLTAuMSAwLjFjLTAuMSAwLjEtMC4yIDAuMi0wLjIgMC4zdjAuMWMtMC4xIDAuMS0wLjEgMC4yLTAuMSAwLjN2MjJjMCAwLjQgMC4yIDAuOCAwLjYgMC45bDkgNGMwLjEgMC4xIDAuMyAwLjEgMC40IDAuMSAwLjIgMCAwLjQtMC4xIDAuNS0wLjIgMC4zLTAuMiAwLjUtMC41IDAuNS0wLjh2LTNoN2MwLjYgMCAxLTAuNCAxLTF2LTEwaDUuNmwtMi4zIDIuM2MtMC40IDAuNC0wLjQgMSAwIDEuNCAwLjIgMC4yIDAuNSAwLjMgMC43IDAuM3MwLjUtMC4xIDAuNy0wLjNsNC00YzAuMS0wLjEgMC4yLTAuMiAwLjItMC4zIDAuMS0wLjMgMC4xLTAuNSAwLTAuOHptLTIwLjkgNy40YzAgMC42LTAuNCAxLTEgMXMtMS0wLjQtMS0xdi00YzAtMC42IDAuNC0xIDEtMXMxIDAuNCAxIDF6bTEwLTExdjE0aC02di0xN2MwLTAuNC0wLjItMC44LTAuNi0wLjlsLTQuNy0yLjFoMTEuM3oiLz48L3N2Zz4K"
        },
        3698: e => {
          e.exports =
            "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjQwIiBoZWlnaHQ9IjQ4MCIgY2xpcC1wYXRoPSJ1cmwoI3ByZXNlbnRhdGlvbl9jbGlwX3BhdGgpIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIHN0cm9rZS13aWR0aD0iMjguMjIyIiBwcmVzZXJ2ZUFzcGVjdFJhdGlvPSJ4TWlkWU1pZCIgdmVyc2lvbj0iMS4yIiB2aWV3Qm94PSIwIDAgNjQwIDQ4MCIgeG1sOnNwYWNlPSJwcmVzZXJ2ZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZGVmcyBjbGFzcz0iQ2xpcFBhdGhHcm91cCI+PGNsaXBQYXRoIGlkPSJwcmVzZW50YXRpb25fY2xpcF9wYXRoIj48cmVjdCB3aWR0aD0iNGUzIiBoZWlnaHQ9IjNlMyIvPjwvY2xpcFBhdGg+PC9kZWZzPjxnIHRyYW5zZm9ybT0idHJhbnNsYXRlKDAgMTM3NzMpIi8+PHBhdGggZD0ibTAgMHY0ODBoNjQwdi00ODBoLTY0MHptMzIwIDIwYTE4MCAyMTUgMCAwIDEgMTgwIDIxNSAxODAgMjE1IDAgMCAxLTE4MCAyMTUgMTgwIDIxNSAwIDAgMS0xODAtMjE1IDE4MCAyMTUgMCAwIDEgMTgwLTIxNXoiIGZpbGwtb3BhY2l0eT0iLjQ5ODA0Ii8+PHBhdGggZD0ibTMyMCAyMGExODAgMjE1IDAgMCAwLTE4MCAyMTUgMTgwIDIxNSAwIDAgMCAxODAgMjE1IDE4MCAyMTUgMCAwIDAgMTgwLTIxNSAxODAgMjE1IDAgMCAwLTE4MC0yMTV6bTAgMTEuODI0YTE3MC4xIDIwMy4xNyAwIDAgMSAxNzAuMSAyMDMuMTggMTcwLjEgMjAzLjE3IDAgMCAxLTE3MC4xIDIwMy4xOCAxNzAuMSAyMDMuMTcgMCAwIDEtMTcwLjEtMjAzLjE4IDE3MC4xIDIwMy4xNyAwIDAgMSAxNzAuMS0yMDMuMTh6IiBmaWxsPSIjZmYwZjBmIiBmaWxsLW9wYWNpdHk9Ii43ODQzMSIvPjwvc3ZnPg=="
        },
        2583: e => {
          e.exports =
            "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbDpzcGFjZT0icHJlc2VydmUiIHZpZXdCb3g9IjAgMCAzNTcgMzU3IiBmaWxsPSIjZmZmIj48cGF0aCBkPSJNMCwyODAuNWg3Ni41VjM1N2g1MVYyMjkuNUgwVjI4MC41eiBNNzYuNSw3Ni41SDB2NTFoMTI3LjVWMGgtNTFWNzYuNXogTTIyOS41LDM1N2g1MXYtNzYuNUgzNTd2LTUxSDIyOS41VjM1N3ogTTI4MC41LDc2LjVWMGgtNTF2MTI3LjVIMzU3di01MUgyODAuNXoiLz48L3N2Zz4="
        },
        4561: e => {
          e.exports =
            "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbDpzcGFjZT0icHJlc2VydmUiIHZpZXdCb3g9IjAgMCAzNTcgMzU3IiBmaWxsPSIjZmZmIj48cGF0aCBkPSJNNTEsMjI5LjVIMFYzNTdoMTI3LjV2LTUxSDUxVjIyOS41eiBNMCwxMjcuNWg1MVY1MWg3Ni41VjBIMFYxMjcuNXogTTMwNiwzMDZoLTc2LjV2NTFIMzU3VjIyOS41aC01MVYzMDZ6IE0yMjkuNSwwdjUxIEgzMDZ2NzYuNWg1MVYwSDIyOS41eiIvPjwvc3ZnPg=="
        },
        3244: e => {
          e.exports =
            "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbDpzcGFjZT0icHJlc2VydmUiIGZpbGw9IiMwMDAiIHZpZXdCb3g9IjAgMCAzMDYuNzcgMzA2Ljc3Ij48cGF0aCBkPSJtMzAyLjkzIDE0OS43OWM1LjU2MS02LjExNiA1LjAyNC0xNS40OS0xLjE5OS0yMC45MzJsLTEzNy4xLTExOS45NmMtNi4yMjMtNS40NDItMTYuMi01LjMyOC0yMi4yOTIgMC4yNTdsLTEzNy41NyAxMjYuMWMtNi4wOTIgNS41ODUtNi4zOTEgMTQuOTQ3LTAuNjYyIDIwLjkwMmwzLjQ0OSAzLjU5MmM1LjcyMiA1Ljk1NSAxNC45NzEgNi42NjUgMjAuNjQ1IDEuNTgxbDEwLjI4MS05LjIwN3YxMzQuNzljMCA4LjI3IDYuNzAxIDE0Ljk2NSAxNC45NjUgMTQuOTY1aDUzLjYyNGM4LjI2NCAwIDE0Ljk2NS02LjY5NSAxNC45NjUtMTQuOTY1di05NC4zaDY4LjM5OHY5NC4zYy0wLjExOSA4LjI2NCA1Ljc5NCAxNC45NTkgMTQuMDU4IDE0Ljk1OWg1Ni44MjhjOC4yNjQgMCAxNC45NjUtNi42OTUgMTQuOTY1LTE0Ljk2NXYtMTMyLjg5czIuODQgMi40ODggNi4zNDMgNS41NjdjMy40OTcgMy4wNzMgMTAuODQyIDAuNjA5IDE2LjQwMy01LjUxM3oiLz48L3N2Zz4="
        },
        3824: e => {
          e.exports =
            "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbDpzcGFjZT0icHJlc2VydmUiIHZpZXdCb3g9IjAgMCA0MjguMDUgNDI4LjA1IiBmaWxsPSIjZmZmIj48cG9seWdvbiBwb2ludHM9IjM3MS4xNSAxOTcuODcgNDA2LjAzIDE3MC42NyAyMTQuMDMgMjEuMzMzIDE1MS44NCA2OS42NTMgMzE5Ljg0IDIzNy42NSIvPjxwb2x5Z29uIHBvaW50cz0iMjcuODkzIDAgMC42OTMgMjcuMiA5MC43MiAxMTcuMjMgMjIuMDI3IDE3MC42NyA1Ni44IDE5Ny42NSAyMTQuMDMgMzIwIDI1OC43MiAyODUuMjMgMjg5LjEyIDMxNS42MyAyMTMuODEgMzc0LjE5IDU2LjU4NyAyNTEuODQgMjIuMDI3IDI3OC43MiAyMTQuMDMgNDI4LjA1IDMxOS41MiAzNDUuOTIgNDAwLjI3IDQyNi42NyA0MjcuMzYgMzk5LjQ3Ii8+PHBvbHlnb24gcG9pbnRzPSIzODAuNjQgMjk4LjQ1IDQwNi4wMyAyNzguNzIgMzc1LjYzIDI0OC4zMiAzNTAuMjQgMjY4LjA1Ii8+PC9zdmc+"
        },
        1686: e => {
          e.exports =
            "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbDpzcGFjZT0icHJlc2VydmUiIHZpZXdCb3g9IjAgMCA0MDYuNzIgNDA2LjcyIiBmaWxsPSIjZmZmIj48cG9seWdvbiBwb2ludHM9IjIwMy4yNSAzNTIuODUgMjAzLjI1IDM1Mi44NSA0NS45MiAyMzAuNTEgMTEuMzYgMjU3LjM5IDIwMy4zNiA0MDYuNzIgMzk1LjM2IDI1Ny4zOSAzNjAuNTkgMjMwLjQiLz48cG9seWdvbiBwb2ludHM9IjIwMy4zNiAyOTguNjcgMzYwLjQ4IDE3Ni41MyAzOTUuMzYgMTQ5LjMzIDIwMy4zNiAwIDExLjM2IDE0OS4zMyA0Ni4xMzMgMTc2LjMyIi8+PC9zdmc+"
        },
        1566: e => {
          e.exports =
            "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbDpzcGFjZT0icHJlc2VydmUiIHZpZXdCb3g9IjAgMCA1MTEuNzEgNTExLjcxIj48cGF0aCBkPSJNMC40OTYsMzk1LjcyOGMwLDE3LjY2NCwxNC4zMiwzMiwzMiwzMkg0MTJjMTcuNjY0LDAsMzItMTQuMzM2LDMyLTMyVjEwNy4yNjRIMC40OTZWMzk1LjcyOHoiIGZpbGw9IiNGM0YzRjMiLz48cGF0aCBkPSJtMjIzLjkgMTk3LjIyaC04Mi42MDhjLTExLjgwOCAwLTIxLjE2OC05LjI2NC0yMC40NDgtMjAuMjcyIDAuMDMyLTAuNDk2IDAuMDQ4LTAuOTc2IDAuMDQ4LTEuNDcydi0wLjI1NmMtMC4wNjQtMTEuMTY4IDkuNjY0LTIwLjI4OCAyMS42MzItMjAuMjg4aDExLjU2OGMxNC4yNzIgMCAyNS44NTYtMTAuOCAyNS44NTYtMjQuMTI4cy0xMS41ODQtMjQuMTQ0LTI1Ljg1Ni0yNC4xNDRoLTE1My42djI5MC4zOGMwIDE3LjY4IDE0LjMyIDMyIDMyIDMyaDExOS42MmMxNC43MzYgMCAyNi42MDgtMTEuNTIgMjUuODI0LTI1LjQ0LTAuNzM2LTEzLjA1Ni0xMy4yOC0yMi44MzItMjcuMjgtMjIuODMyaC0yMS4zNzZjLTEyLjQ5NiAwLTIxLjgwOC05Ljc5Mi0yMS42NjQtMjEuNDU2di0wLjI4OHMwLTAuMTkyIDAtMC4yODhjLTAuMTQ0LTExLjY2NCA5LjE2OC0yMS40NTYgMjEuNjY0LTIxLjQ1Nmg1My4wNTZjMTQuNzM2IDAgMjYuNjA4LTExLjUyIDI1LjgyNC0yNS40NC0wLjczNi0xMy4wNTYtMTMuMjgtMjIuODMyLTI3LjI4LTIyLjgzMmgtMjguMjg4Yy0xMi42NCAwLTIyLjkyOC05LjY2NC0yMi44NjQtMjEuNDU2di0wLjI4OGwtMC4wMTYtMS4zOTJjLTAuMDgtMTEuMjE2IDkuNjQ4LTIwLjM1MiAyMS42OC0yMC4zNTJoNzMuOTY4YzE0LjczNiAwIDI2LjYwOC0xMS41MiAyNS44MjQtMjUuNDQtMC43Mi0xMy4wODgtMTMuMjgtMjIuODY0LTI3LjI4LTIyLjg2NHoiIGZpbGw9IiNFOEU4RTgiLz48cGF0aCBkPSJtNDc2LjI3IDI1My4yMmMwLTQ5LjU4NC00MC4zMi04OS45MDQtODkuOTA0LTg5LjkwNHMtODkuOTIgNDAuMzM2LTg5LjkyIDg5LjkwNHYxMDQuOTNoMjB2LTEwNC45MWMwLTM4LjYwOCAzMS4yOTYtNjkuOTIgNjkuOTA0LTY5LjkyczY5LjkwNCAzMS4yOTYgNjkuOTA0IDY5LjkydjEwNC45MWgyMHYtMTA0LjkzaDAuMDE2eiIgZmlsbD0iI0MwQkZCRiIvPjxwYXRoIGQ9Im0zODYuMzcgMTgzLjMxYy0zOC42MDggMC02OS45MDQgMzEuMjk2LTY5LjkwNCA2OS45MnYxMDQuOTFoMTM5Ljgydi0xMDQuOTFjLTAuMDE2LTM4LjYyNC0zMS4zMTItNjkuOTItNjkuOTItNjkuOTJ6bS00OS45MiAxMzQuODJ2LTY0LjkyOGMwLTI3LjUyIDIyLjM4NC00OS45MDQgNDkuOTItNDkuOTA0IDI3LjUyIDAgNDkuOTA0IDIyLjM4NCA0OS45MDQgNDkuOTA0djY0LjkyOGgtOTkuODI0eiIgZmlsbD0iI0NBQ0FDQSIvPjxwYXRoIGQ9Im00NzkuMjIgMzA4LjkxaC0xODUuN2MtMTcuNjggMC0zMiAxNC4zMi0zMiAzMnYxMzguNzdjMCAxNy42OCAxNC4zMiAzMiAzMiAzMmgxODUuN2MxNy42OCAwIDMyLTE0LjMyIDMyLTMydi0xMzguNzdjMC0xNy42NjQtMTQuMzItMzItMzItMzJ6IiBmaWxsPSIjRkRCQzRCIi8+PHBhdGggZD0ibTUxMS4xMiA0NzkuNjh2LTEzOC43N2MwLTE3LjY4LTE0LjMzNi0zMi0zMi0zMmgtNDEuMTY4Yy04Ljk3NiAwLTE2LjI3MiA2LjgtMTYuMjcyIDE1LjE4NHM3LjI4IDE1LjE4NCAxNi4yNzIgMTUuMTg0aDcuMjhjNy41MiAwIDEzLjY0OCA1Ljc0NCAxMy42IDEyLjc2OHYwLjE2YzAgMC4zMDQgMC4wMTYgMC42MjQgMC4wMzIgMC45MjggMC40NDggNi45MjgtNS40NCAxMi43NTItMTIuODY0IDEyLjc1MmgtNTEuOTUyYy04LjggMC0xNi43MDQgNi4xNi0xNy4xNjggMTQuMzY4LTAuNDk2IDguNzUyIDYuOTYgMTYgMTYuMjQgMTZoNDYuNTI4YzcuNTY4IDAgMTMuNjggNS43NDQgMTMuNjMyIDEyLjh2MS4wNTZjMC4wNDggNy40MjQtNi40MTYgMTMuNTA0LTE0LjM4NCAxMy41MDRoLTE3Ljc3NmMtOC44IDAtMTYuNzA0IDYuMTYtMTcuMTY4IDE0LjM2OC0wLjQ5NiA4Ljc1MiA2Ljk2IDE2IDE2LjI0IDE2aDMzLjM2YzcuODU2IDAgMTMuNzEyIDYuMTYgMTMuNjMyIDEzLjUwNHYwLjE3NiAwLjE3NmMwLjA5NiA3LjMyOC01Ljc2IDEzLjUwNC0xMy42MzIgMTMuNTA0aC0xMy40NGMtOC44IDAtMTYuNzA0IDYuMTYtMTcuMTY4IDE0LjM2OC0wLjQ5NiA4Ljc1MiA2Ljk2IDE2IDE2LjI0IDE2aDM5LjkyYzE3LjY5Ni0wLjAzMiAzMi4wMTYtMTQuMzUyIDMyLjAxNi0zMi4wMzJ6IiBmaWxsPSIjRkZDQzVCIi8+PHBhdGggZD0ibTQxNy40MSAzOTMuODJjMC0xNy4xNTItMTMuOTA0LTMxLjA1Ni0zMS4wNTYtMzEuMDU2cy0zMS4wNTYgMTMuOTA0LTMxLjA1NiAzMS4wNTZjMCAxMi4wMzIgNi45MjggMjIuMzUyIDE2LjkyOCAyNy41MDRsLTYuNzA0IDM2LjQ5Nmg0MS42NDhsLTYuNzA0LTM2LjQ5NmMxMC4wMzItNS4xNTIgMTYuOTQ0LTE1LjQ3MiAxNi45NDQtMjcuNTA0eiIgZmlsbD0iIzQ2NDY0NiIvPjxwYXRoIGQ9Im00NDQgMTA3LjI2di03NS4yNjRjMC0xNy42OC0xNC4zMzYtMzItMzItMzJoLTM3OS41Yy0xNy42OCAwLTMyIDE0LjMyLTMyIDMydjc1LjI2NGg0NDMuNXoiIGZpbGw9IiM2RjcwNzAiLz48Y2lyY2xlIGN4PSI1OC43MzYiIGN5PSI1My42MzIiIHI9IjIwLjY1NiIgZmlsbD0iI2ZmZiIvPjxjaXJjbGUgY3g9IjExNy4wNiIgY3k9IjUzLjYzMiIgcj0iMjAuNjU2IiBmaWxsPSIjRkZFMjhGIi8+PGNpcmNsZSBjeD0iMTc1LjM4IiBjeT0iNTMuNjMyIiByPSIyMC42NTYiIGZpbGw9IiNGREJDNEIiLz48ZyBmaWxsPSIjNzg3ODc4Ij48cGF0aCBkPSJtMzE1LjA2IDUzLjYzMmMwIDguODMyIDcuMTUyIDE2IDE2IDE2aDQ0LjA2NGM4Ljg0OCAwIDE2LTcuMTY4IDE2LTE2cy03LjE1Mi0xNi0xNi0xNmgtNDQuMDY0Yy04Ljg0OCAwLTE2IDcuMTY4LTE2IDE2eiIvPjxwYXRoIGQ9Im0yNDguNjkgNTMuNjMyYzAgOC44MzIgNy4xNTIgMTYgMTYgMTZoMTguNzM2YzguODQ4IDAgMTYtNy4xNjggMTYtMTZzLTcuMTUyLTE2LTE2LTE2aC0xOC43MzZjLTguODQ4IDAtMTYgNy4xNjgtMTYgMTZ6Ii8+PC9nPjwvc3ZnPg=="
        },
        5746: e => {
          e.exports =
            "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbDpzcGFjZT0icHJlc2VydmUiIHZpZXdCb3g9IjAgMCA0ODQuNSA0ODQuNSIgZmlsbD0iI2ZmZiI+PHBhdGggZD0ibTQyMC43NSAyMjkuNWgtNDMuMzVjMCAxNy44NS01LjEwMSAzNS43LTEwLjIgNTFsMzAuNiAzMC42YzE1LjMtMjIuOTUgMjIuOTUtNTEgMjIuOTUtODEuNnoiLz48cGF0aCBkPSJtMzE4Ljc1IDIzNC42di01LjEtMTUzYzAtNDMuMzUtMzMuMTUtNzYuNS03Ni41LTc2LjVzLTc2LjUgMzMuMTUtNzYuNSA3Ni41djUuMWwxNTMgMTUzeiIvPjxwYXRoIGQ9Im00NS45IDI1LjUtMzMuMTUgMzMuMTUgMTUzIDE1M3YxNy44NWMwIDQzLjM1IDMzLjE1IDc2LjUgNzYuNSA3Ni41IDUuMSAwIDEwLjIgMCAxNy44NS0yLjU1bDQzLjM1MSA0My4zNWMtMTcuODUxIDcuNjUtMzguMjUgMTIuNzUtNTguNjUgMTIuNzUtNzEuNCAwLTEzNS4xNS01My41NS0xMzUuMTUtMTMwLjA1aC00NS45YzAgODYuNyA2OC44NSAxNTguMSAxNTMgMTcwLjg1djg0LjE1aDUxdi04NC4xNWMyMi45NS0yLjU1IDQ1LjktMTIuNzUgNjMuNzUtMjIuOTQ5bDEwNy4xIDEwNy4xIDMzLjE1LTMzLjE1LTQyNS44NS00MjUuODV6Ii8+PC9zdmc+"
        },
        4541: e => {
          e.exports =
            "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbDpzcGFjZT0icHJlc2VydmUiIHZpZXdCb3g9IjAgMCA0ODQuNSA0ODQuNSIgZmlsbD0iI2ZmZiI+PHBhdGggZD0ibTI0Mi4yNSAzMDZjNDMuMzUgMCA3Ni41LTMzLjE1IDc2LjUtNzYuNXYtMTUzYzAtNDMuMzUtMzMuMTUtNzYuNS03Ni41LTc2LjVzLTc2LjUgMzMuMTUtNzYuNSA3Ni41djE1M2MwIDQzLjM1IDMzLjE1IDc2LjUgNzYuNSA3Ni41em0xMzUuMTUtNzYuNWMwIDc2LjUtNjMuNzUgMTMwLjA1LTEzNS4xNSAxMzAuMDVzLTEzNS4xNS01My41NS0xMzUuMTUtMTMwLjA1aC00My4zNWMwIDg2LjcgNjguODUgMTU4LjEgMTUzIDE3MC44NXY4NC4xNWg1MXYtODQuMTVjODQuMTUtMTIuNzUgMTUzLTg0LjE0OSAxNTMtMTcwLjg1aC00My4zNXoiLz48L3N2Zz4="
        },
        2894: e => {
          e.exports =
            "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjQwIiBoZWlnaHQ9IjQ4MCIgY2xpcC1wYXRoPSJ1cmwoI3ByZXNlbnRhdGlvbl9jbGlwX3BhdGgpIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIHN0cm9rZS13aWR0aD0iMjguMjIyIiBwcmVzZXJ2ZUFzcGVjdFJhdGlvPSJ4TWlkWU1pZCIgdmVyc2lvbj0iMS4yIiB2aWV3Qm94PSIwIDAgNjQwIDQ4MCIgeG1sOnNwYWNlPSJwcmVzZXJ2ZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZGVmcyBjbGFzcz0iQ2xpcFBhdGhHcm91cCI+PGNsaXBQYXRoIGlkPSJwcmVzZW50YXRpb25fY2xpcF9wYXRoIj48cmVjdCB3aWR0aD0iNGUzIiBoZWlnaHQ9IjNlMyIvPjwvY2xpcFBhdGg+PC9kZWZzPjxwYXRoIGQ9Im0wIDB2NDgwaDY0MHYtNDgwem00MS4xMDIgNDBoNTU3LjhjMC42MTAzMyAwIDEuMTAxNiAwLjQ5MTIzIDEuMTAxNiAxLjEwMTZ2Mzk3LjhjMCAwLjYxMDMzLTAuNDkxMjMgMS4xMDE2LTEuMTAxNiAxLjEwMTZoLTU1Ny44Yy0wLjYxMDMzIDAtMS4xMDE2LTAuNDkxMjMtMS4xMDE2LTEuMTAxNnYtMzk3LjhjMC0wLjYxMDMzIDAuNDkxMjMtMS4xMDE2IDEuMTAxNi0xLjEwMTZ6IiBmaWxsLW9wYWNpdHk9Ii40OTgwNCIvPjxwYXRoIGQ9Im00MS41IDQwYy0wLjgzMSAwLTEuNSAwLjY2OS0xLjUgMS41djM5N2MwIDAuODMxIDAuNjY5IDEuNSAxLjUgMS41aDU1N2MwLjgzMSAwIDEuNS0wLjY2OSAxLjUtMS41di0zOTdjMC0wLjgzMS0wLjY2OS0xLjUtMS41LTEuNWgtNTU3em05Ljk0NzMgMTBoNTM3LjExYzAuODAxMzIgMCAxLjQ0NzMgMC42MzYzMyAxLjQ0NzMgMS40MjU4djM3Ny4xNWMwIDAuNzg5NDUtMC42NDU5NSAxLjQyNTgtMS40NDczIDEuNDI1OGgtNTM3LjExYy0wLjgwMTMyIDAtMS40NDczLTAuNjM2MzMtMS40NDczLTEuNDI1OHYtMzc3LjE1YzAtMC43ODk0NSAwLjY0NTk0LTEuNDI1OCAxLjQ0NzMtMS40MjU4eiIgZmlsbD0iI2ZmMGYwZiIgZmlsbC1vcGFjaXR5PSIuNzg0MzEiIGZpbGwtcnVsZT0iZXZlbm9kZCIgc3Ryb2tlLW1pdGVybGltaXQ9IjAiIHN0cm9rZS13aWR0aD0iMCIvPjwvc3ZnPg=="
        },
        2675: e => {
          e.exports =
            "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbDpzcGFjZT0icHJlc2VydmUiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0iIzAwMCI+PHBhdGggZD0iTTAgMGgyNHYyNEgweiIgZmlsbD0ibm9uZSIvPjxwYXRoIGQ9Im0xNy4xODMgMTguNDc4di0xLjI5NTdoLTMuODg3di0zLjg4N2gzLjg4N3YyLjU5MTRoMi41OTE0djIuNTkxNGgtMS4yOTU3djIuNTkxNGgtMi41OTE0djIuNTkxNGgtMi41OTE0di0zLjg4NzFoMi41OTE0di0xLjI5NTd6bTYuNDc4NCA1LjE4MjdoLTUuMTgyN3YtMi41OTE0aDIuNTkxNHYtMi41OTE0aDIuNTkxNHptLTIzLjMyMi0yMy4zMjJoMTAuMzY1djEwLjM2NWgtMTAuMzY1em0yLjU5MTQgMi41OTE0djUuMTgyN2g1LjE4Mjd2LTUuMTgyN3ptMTAuMzY1LTIuNTkxNGgxMC4zNjV2MTAuMzY1aC0xMC4zNjV6bTIuNTkxNCAyLjU5MTR2NS4xODI3aDUuMTgyN3YtNS4xODI3em0tMTUuNTQ4IDEwLjM2NWgxMC4zNjV2MTAuMzY1aC0xMC4zNjV6bTIuNTkxNCAyLjU5MTR2NS4xODI3aDUuMTgyN3YtNS4xODI3em0xNi44NDQtMi41OTE0aDMuODg3MXYyLjU5MTRoLTMuODg3MXptLTE1LjU0OC05LjA2OThoMi41OTE0djIuNTkxNGgtMi41OTE0em0wIDEyLjk1N2gyLjU5MTR2Mi41OTE0aC0yLjU5MTR6bTEyLjk1Ny0xMi45NTdoMi41OTE0djIuNTkxNGgtMi41OTE0eiIgc3Ryb2tlLXdpZHRoPSIxLjI5NTciLz48L3N2Zz4K"
        },
        368: e => {
          e.exports =
            "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbDpzcGFjZT0icHJlc2VydmUiIHZpZXdCb3g9IjAgMCA1NjEgNTYxIiBmaWxsPSIjZmZmIj48cGF0aCBkPSJtNTEwIDUxaC00NTljLTI4LjA1IDAtNTEgMjIuOTUtNTEgNTF2NzYuNWg1MXYtNzYuNWg0NTl2MzU3aC0xNzguNXY1MWgxNzguNWMyOC4wNSAwIDUxLTIyLjk1IDUxLTUxdi0zNTdjMC0yOC4wNS0yMi45NS01MS01MS01MXptLTUxMCAzODIuNXY3Ni41aDc2LjVjMC00My4zNS0zMy4xNS03Ni41LTc2LjUtNzYuNXptMC0xMDJ2NTFjNzEuNCAwIDEyNy41IDU2LjEgMTI3LjUgMTI3LjVoNTFjMC05OS40NS03OS4wNS0xNzguNS0xNzguNS0xNzguNXptMC0xMDJ2NTFjMTI3LjUgMCAyMjkuNSAxMDIgMjI5LjUgMjI5LjVoNTFjMC0xNTUuNTUtMTI0Ljk1LTI4MC41LTI4MC41LTI4MC41eiIvPjwvc3ZnPg=="
        },
        390: e => {
          e.exports =
            "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbDpzcGFjZT0icHJlc2VydmUiIHZpZXdCb3g9IjAgMCA1NjEgNTYxIiBmaWxsPSIjZmZmIj48cGF0aCBkPSJtMCA0MzMuNXY3Ni41aDc2LjVjMC00My4zNS0zMy4xNS03Ni41LTc2LjUtNzYuNXptMC0xMDJ2NTFjNzEuNCAwIDEyNy41IDU2LjEgMTI3LjUgMTI3LjVoNTFjMC05OS40NS03OS4wNS0xNzguNS0xNzguNS0xNzguNXptNDU5LTE3OC41aC0zNTd2NDAuOGMxMDIgMzMuMTUgMTgxLjA1IDExMi4yIDIxNC4yIDIxNC4yaDE0Mi44di0yNTV6bS00NTkgNzYuNXY1MWMxMjcuNSAwIDIyOS41IDEwMiAyMjkuNSAyMjkuNWg1MWMwLTE1NS41NS0xMjQuOTUtMjgwLjUtMjgwLjUtMjgwLjV6bTUxMC0xNzguNWgtNDU5Yy0yOC4wNSAwLTUxIDIyLjk1LTUxIDUxdjc2LjVoNTF2LTc2LjVoNDU5djM1N2gtMTc4LjV2NTFoMTc4LjVjMjguMDUgMCA1MS0yMi45NSA1MS01MXYtMzU3YzAtMjguMDUtMjIuOTUtNTEtNTEtNTF6Ii8+PC9zdmc+"
        },
        9046: e => {
          e.exports =
            "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbDpzcGFjZT0icHJlc2VydmUiIHZpZXdCb3g9IjAgMCA1MTIgNTEyIiBmaWxsPSIjODA4MDgwIj48ZyB0cmFuc2Zvcm09Im1hdHJpeCgxLjE3MDggMCAwIDEuMTgyOCAuMDAxNzY4IC0yLjYxMTgpIj48Zz48cGF0aCBkPSJtNDMyLjcxIDYuNzk4Yy00LjYwOC00LjYwOC0xMC4yNC01LjYzMi0xNS4zNi0zLjU4NGwtMzQ0LjU4IDEzOC4yNGMtNS42MzIgMi4wNDgtOS4yMTYgOC4xOTItOS4yMTYgMTMuODI0czQuNjA4IDExLjI2NCAxMC4yNCAxMy4zMTJsMTUxLjA0IDQ2LjU5MiA0Ni41OTIgMTUwLjUzYzEuNTM2IDUuNjMyIDYuNjU2IDkuNzI4IDEzLjMxMiAxMC4yNGgwLjUxMmM1LjYzMiAwIDEwLjc1Mi0zLjU4NCAxMy4zMTItOS4yMTZsMTM3LjczLTM0NC41OGMyLjA0OC01LjEyIDEuMDI0LTExLjI2NC0zLjU4NC0xNS4zNnoiLz48L2c+PC9nPjxnID48ZyB0cmFuc2Zvcm09Im1hdHJpeCgxLjE3MDggMCAwIDEuMTgyOCAuMDAxNzY4IC0yLjYxMTgpIj48Zz48cmVjdCB0cmFuc2Zvcm09Im1hdHJpeCguNzA3MSAtLjcwNzEgLjcwNzEgLjcwNzEgLTIxOC44OSAxNjQuMzkpIiB4PSIzNS40ODYiIHk9IjMzMi4wOCIgd2lkdGg9IjEwNy4wMSIgaGVpZ2h0PSIyOC42NzIiLz48L2c+PC9nPjxnIHRyYW5zZm9ybT0ibWF0cml4KDEuMTcwOCAwIDAgMS4xODI4IC4wMDE3NjggLTIuNjExOCkiPjxnPjxyZWN0IHRyYW5zZm9ybT0ibWF0cml4KC43MDcxIC0uNzA3MSAuNzA3MSAuNzA3MSAtMTczLjM2IDExMS41NSkiIHg9Ii01LjUzNCIgeT0iMjUwLjciIHdpZHRoPSIxMDcuMDEiIGhlaWdodD0iMjguNjcyIi8+PC9nPjwvZz48ZyB0cmFuc2Zvcm09Im1hdHJpeCgxLjE3MDggMCAwIDEuMTgyOCAuMDAxNzY4IC0yLjYxMTgpIj48Zz48cmVjdCB0cmFuc2Zvcm09Im1hdHJpeCguNzA3MSAtLjcwNzEgLjcwNzEgLjcwNzEgLTIyMy44OCAyMzMuNzUpIiB4PSIxMTYuNzIiIHk9IjM3Mi43OCIgd2lkdGg9IjEwNy4wMSIgaGVpZ2h0PSIyOC42NzIiLz48L2c+PC9nPjwvZz48L3N2Zz4="
        },
        8260: e => {
          e.exports =
            "data:image/gif;base64,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"
        },
        1647: e => {
          e.exports =
            "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbDpzcGFjZT0icHJlc2VydmUiIHZpZXdCb3g9IjAgMCA0MTYuMyA0MTYuMyIgZmlsbD0iIzAwMDAwMCI+PHBhdGggZD0ibTM0OC43NSAyNjEuN2MtMC42NC0wLjY0LTEuMzI4LTEuMi0yLjA2NC0xLjYzMi0xMC4zNjgtNi41MjgtMjIuMTkyLTkuODI0LTM0LjAxNi05LjgyNC0xNi4zNjggMC0zMi43MiA2LjI0LTQ1LjIgMTguNzJsLTExLjMyOCAxMS4zMTJ2LTE1Mi4yNGMwLTE3LjYtMTQuNC0zMi0zMi0zMnMtMzIgMTQuNC0zMiAzMnY3MC40Yy01Ljg0LTcuMTY4LTE0LjY0LTExLjg0LTI0LjYwOC0xMS44NC02LjkyOCAwLTEzLjMxMiAyLjI3Mi0xOC41NDQgNi4wMzJsLTY4LjkxMiAzOS44ODhjLTkuNTIgNS41NjgtMTUuOTM2IDE1Ljc5Mi0xNS45MzYgMjcuNTg0djUyLjYyNGMwIDU3LjIxNiA0Ni4zNjggMTAzLjU4IDEwMy41OCAxMDMuNTggMjcuNzEyIDAgNTIuODE2LTEwLjk0NCA3MS4zOTItMjguNjcybDAuMDE2IDAuMTQ0IDEuODU2LTEuODU2IDEwNy43NC0xMDcuNzZjNC41Ni00LjU2IDQuNTYtMTEuOTA0IDAuMDE2LTE2LjQ2NHptLTEyMC42NyAxMTQuMzRjLTE2LjQgMTUuNjMyLTM3Ljg0IDI0LjI0LTYwLjM1MiAyNC4yNC00OC4yODggMC4wMzItODcuNTg0LTM5LjI4LTg3LjU4NC04Ny41Njh2LTUyLjYyNGMwLTUuNjMyIDIuOTkyLTEwLjczNiA4LjAxNi0xMy42NjRsNzAuMTQ0LTQwLjc4NGMxLjkyLTEuMzc2IDUuMDg4LTMuMDQgOS4yMTYtMy4wNCA2LjQgMCAxMC40IDMuNzI4IDEyLjIyNCA1Ljk1MmwyOC40IDM0Ljc4NHYtMTE1LjNjMC04LjgxNiA3LjE4NC0xNiAxNi0xNnMxNiA3LjE4NCAxNiAxNnYxNTkuOTVjMCA2LjgzMiA0LjMyIDEyLjU2IDEwLjM1MiAxNC44MTYgMi41NDQgMC45NiA1LjQwOCAwLjMzNiA3LjMyOC0xLjU4NGwyMC45NDQtMjAuOTQ0YzkuMDU2LTkuMDU2IDIxLjA4OC0xNC4wMzIgMzMuODg4LTE0LjAzMiA3LjIxNiAwIDE0LjI3MiAxLjYgMjAuNzA0IDQuNjcybC0xMDUuMjggMTA1LjEyeiIvPjxyZWN0IHg9IjIxNi4xNCIgd2lkdGg9IjE2IiBoZWlnaHQ9IjY0Ii8+PHJlY3QgdHJhbnNmb3JtPSJtYXRyaXgoLjcwNzEgLS43MDcxIC43MDcxIC43MDcxIDMuMjY2MSAxMjguMDkpIiB4PSIxNDguMjYiIHk9IjI4LjEwNSIgd2lkdGg9IjE2IiBoZWlnaHQ9IjYzLjk5OSIvPjxyZWN0IHg9Ijk2LjE0NSIgeT0iMTIwIiB3aWR0aD0iNjQiIGhlaWdodD0iMTYiLz48cmVjdCB0cmFuc2Zvcm09Im1hdHJpeCguNzA3MSAtLjcwNzEgLjcwNzEgLjcwNzEgNDMuMDEyIDIyNC4wOSkiIHg9IjI2MC4wMSIgeT0iNTIuMTI2IiB3aWR0aD0iNjMuOTk5IiBoZWlnaHQ9IjE2Ii8+PHJlY3QgeD0iMjg4LjE0IiB5PSIxMjAiIHdpZHRoPSI2NCIgaGVpZ2h0PSIxNiIvPjwvc3ZnPg=="
        },
        5494: e => {
          e.exports =
            "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbDpzcGFjZT0icHJlc2VydmUiIHZpZXdCb3g9IjAgMCA1MTIgNTEyIiBmaWxsPSIjODA4MDgwIj48ZyB0cmFuc2Zvcm09InRyYW5zbGF0ZSgwLDQ3NikiPjxnIHRyYW5zZm9ybT0ibWF0cml4KDIzLjI3MyAwIDAgMjMuMTU4IC0xMDA1NCAtODY5MCkiPjxwYXRoIGQ9Im00NDkgMzYxLjE3djguODMwOWMwIDEuMTA2MS0wLjg5MDA2IDIuMDAyOC0yLjAwMDEgMi4wMDI4aC04LjgzMzZsLTIuOTU5MiAyLjk1OTJjLTAuMzkwNTMgMC4zOTA1Mi0xLjAyMzcgMC4zOTA1Mi0xLjQxNDIgMC0wLjM5MDUyLTAuMzkwNTMtMC4zOTA1Mi0xLjAyMzcgMC0xLjQxNDJsMTctMTdjMC4zOTA1My0wLjM5MDUyIDEuMDIzNy0wLjM5MDUyIDEuNDE0MiAwIDAuMzkwNTIgMC4zOTA1MyAwLjM5MDUyIDEuMDIzNyAwIDEuNDE0MnptLTIuNjYyMS0yLjE2NjNoLTEyLjMzOGMtMS4xMSAwLTIuMDAwMSAwLjg5NjY3LTIuMDAwMSAyLjAwMjh2OC45OTQ1YzAgMC45MDc1NCAwLjU5OTQ1IDEuNjcwNyAxLjQyMjQgMS45MTgyem0zLjY2MjEgMyA0LTR2MTVsLTQtNHoiLz48L2c+PC9nPjwvc3ZnPg=="
        },
        1952: e => {
          e.exports =
            "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbDpzcGFjZT0icHJlc2VydmUiIHZpZXdCb3g9IjAgMCA0NjEuNTUgNDYxLjU1IiBmaWxsPSIjZmZmIj48cGF0aCBkPSJtMzQ1LjUyIDIyOS41YzAtNDUuOS0yNS41LTg0LjE1LTYzLjc1LTEwMnY1Ni4xbDYzLjc1IDYzLjc1di0xNy44NXptNjMuNzUgMGMwIDIyLjk1LTUuMSA0NS45LTEyLjc1IDY2LjNsMzguMjUgMzguMjVjMTcuODUtMzAuNiAyNS41LTY4Ljg1IDI1LjUtMTA3LjEgMC0xMDkuNjUtNzYuNS0yMDEuNDUtMTc4LjUtMjI0LjR2NTMuNTVjNzMuOTUgMjUuNSAxMjcuNSA5MS44IDEyNy41IDE3My40em0tMzc0Ljg1LTIyOS41LTMzLjE1IDMzLjE1IDExOS44NSAxMTkuODVoLTExOS44NXYxNTNoMTAybDEyNy41IDEyNy41di0xNzAuODVsMTA5LjY1IDEwOS42NWMtMTcuODUxIDEyLjc1LTM1LjcgMjIuOTUtNTguNjUgMzAuNjAxdjUzLjU1YzM1LjctNy42NSA2Ni4zLTIyLjk1IDk0LjM1LTQ1LjlsNTEgNTEgMzMuMTUtMzMuMTQ5LTIyOS41LTIyOS41LTE5Ni4zNS0xOTguOXptMTk2LjM1IDI1LjUtNTMuNTUgNTMuNTUgNTMuNTUgNTMuNTV2LTEwNy4xeiIvPjwvc3ZnPg=="
        },
        8160: e => {
          e.exports =
            "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbDpzcGFjZT0icHJlc2VydmUiIHZpZXdCb3g9IjAgMCA0NTkgNDU5IiBmaWxsPSIjZmZmIj48cGF0aCBkPSJtMCAxNTN2MTUzaDEwMmwxMjcuNSAxMjcuNXYtNDA4bC0xMjcuNSAxMjcuNWgtMTAyem0zNDQuMjUgNzYuNWMwLTQ1LjktMjUuNS04NC4xNS02My43NS0xMDJ2MjA0YzM4LjI1LTE3Ljg1IDYzLjc1LTU2LjEgNjMuNzUtMTAyem0tNjMuNzUtMjI0LjR2NTMuNTVjNzMuOTUgMjIuOTUgMTI3LjUgODkuMjQ5IDEyNy41IDE3MC44NXMtNTMuNTUgMTQ3LjktMTI3LjUgMTcwLjg1djUzLjU1YzEwMi0yMi45NTEgMTc4LjUtMTE0Ljc1IDE3OC41LTIyNC40cy03Ni41LTIwMS40NS0xNzguNS0yMjQuNHoiLz48L3N2Zz4="
        }
      },
      t = {};
  
    function r(i) {
      var n = t[i];
      if (void 0 !== n) return n.exports;
      var o = t[i] = {
        id: i,
        exports: {}
      };
      return e[i](o, o.exports, r), o.exports
    }
    r.m = e, r.n = e => {
      var t = e && e.__esModule ? () => e.default : () => e;
      return r.d(t, {
        a: t
      }), t
    }, r.d = (e, t) => {
      for (var i in t) r.o(t, i) && !r.o(e, i) && Object.defineProperty(e, i, {
        enumerable: !0,
        get: t[i]
      })
    }, r.o = (e, t) => Object.prototype.hasOwnProperty.call(e, t), r.r = e => {
      "undefined" != typeof Symbol && Symbol.toStringTag && Object.defineProperty(e, Symbol.toStringTag, {
        value: "Module"
      }), Object.defineProperty(e, "__esModule", {
        value: !0
      })
    }, r.b = document.baseURI || self.location.href, r.nc = void 0;
    var i = {};
    return (() => {
      r.d(i, {
        default: () => Wo
      });
      var e = {};
      r.r(e), r.d(e, {
        Decoder: () => fe,
        Encoder: () => be,
        PacketType: () => ge,
        protocol: () => he
      });
      var t = {};
      r.r(t), r.d(t, {
        fixNegotiationNeeded: () => vt,
        shimAddTrackRemoveTrack: () => ut,
        shimAddTrackRemoveTrackWithNative: () => dt,
        shimGetDisplayMedia: () => nt,
        shimGetSendersWithDtmf: () => st,
        shimGetStats: () => ct,
        shimGetUserMedia: () => it,
        shimMediaStream: () => ot,
        shimOnTrack: () => at,
        shimPeerConnection: () => pt,
        shimSenderReceiverGetStats: () => lt
      });
      var n = {};
      r.r(n), r.d(n, {
        shimAddTransceiver: () => Pt,
        shimCreateAnswer: () => At,
        shimCreateOffer: () => Lt,
        shimGetDisplayMedia: () => ht,
        shimGetParameters: () => Tt,
        shimGetUserMedia: () => mt,
        shimOnTrack: () => gt,
        shimPeerConnection: () => bt,
        shimRTCDataChannel: () => jt,
        shimReceiverGetStats: () => yt,
        shimRemoveStream: () => Mt,
        shimSenderGetStats: () => ft
      });
      var o = {};
      r.r(o), r.d(o, {
        shimAudioContext: () => Et,
        shimCallbacksAPI: () => Nt,
        shimConstraints: () => Dt,
        shimCreateOfferLegacy: () => xt,
        shimGetUserMedia: () => It,
        shimLocalStreamsAPI: () => wt,
        shimRTCIceServerUrls: () => Ct,
        shimRemoteStreamsAPI: () => kt,
        shimTrackEventTransceiver: () => zt
      });
      var a, s = {};
      r.r(s), r.d(s, {
        removeExtmapAllowMixed: () => Bt,
        shimAddIceCandidateNullOrEmpty: () => Kt,
        shimConnectionState: () => Gt,
        shimMaxMessageSize: () => Yt,
        shimParameterlessSetLocalDescription: () => Ht,
        shimRTCIceCandidate: () => Rt,
        shimRTCIceCandidateRelayProtocol: () => Qt,
        shimSendThrowTypeError: () => Ut
      });
      var c = {
        get: e => e ? e.split(".").reduce((function (e, t) {
          return e ? e[t] : e
        }), a) : a,
        sync: e => a = e
      };
      const l = c;
      var d = {};
      const u = {
          on(e, t) {
            e && t && (e = [].concat(e)).forEach((function (e) {
              d[e] || (d[e] = []), d[e].push(t)
            }))
          },
          off(e, t) {
            if (!e) return d = {};
            (e = [].concat(e)).forEach((function (e) {
              t || delete d[e];
              var r = d[e];
              if (r) {
                var i = r.indexOf(t);
                i > -1 && r.splice(i, 1)
              }
            }))
          },
          dispatchEvent(e, t) {
            var r = d[e];
            if (r) {
              var i = [];
              return r.forEach((function (r) {
                i.push(r.call({
                  event: e
                }, t))
              })), Promise.all(i)
            }
          }
        },
        p = Object.create(null);
      p.open = "0", p.close = "1", p.ping = "2", p.pong = "3", p.message = "4", p.upgrade = "5", p.noop = "6";
      const v = Object.create(null);
      Object.keys(p).forEach((e => {
        v[p[e]] = e
      }));
      const m = {
          type: "error",
          data: "parser error"
        },
        h = "function" == typeof Blob || "undefined" != typeof Blob && "[object BlobConstructor]" === Object
        .prototype.toString.call(Blob),
        g = "function" == typeof ArrayBuffer,
        b = (e, t) => {
          const r = new FileReader;
          return r.onload = function () {
            const e = r.result.split(",")[1];
            t("b" + (e || ""))
          }, r.readAsDataURL(e)
        },
        f = ({
          type: e,
          data: t
        }, r, i) => {
          return h && t instanceof Blob ? r ? i(t) : b(t, i) : g && (t instanceof ArrayBuffer || (n = t,
            "function" == typeof ArrayBuffer.isView ? ArrayBuffer.isView(n) : n && n
            .buffer instanceof ArrayBuffer)) ? r ? i(t) : b(new Blob([t]), i) : i(p[e] + (t || ""));
          var n
        },
        y = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/",
        M = "undefined" == typeof Uint8Array ? [] : new Uint8Array(256);
      for (let e = 0; e < 64; e++) M[y.charCodeAt(e)] = e;
      const j = "function" == typeof ArrayBuffer,
        P = (e, t) => {
          if (j) {
            const r = (e => {
              let t, r, i, n, o, a = .75 * e.length,
                s = e.length,
                c = 0;
              "=" === e[e.length - 1] && (a--, "=" === e[e.length - 2] && a--);
              const l = new ArrayBuffer(a),
                d = new Uint8Array(l);
              for (t = 0; t < s; t += 4) r = M[e.charCodeAt(t)], i = M[e.charCodeAt(t + 1)], n = M[e
                .charCodeAt(t + 2)], o = M[e.charCodeAt(t + 3)], d[c++] = r << 2 | i >> 4, d[c++] = (15 &
                i) << 4 | n >> 2, d[c++] = (3 & n) << 6 | 63 & o;
              return l
            })(e);
            return T(r, t)
          }
          return {
            base64: !0,
            data: e
          }
        },
        T = (e, t) => "blob" === t && e instanceof ArrayBuffer ? new Blob([e]) : e,
        L = (e, t) => {
          if ("string" != typeof e) return {
            type: "message",
            data: T(e, t)
          };
          const r = e.charAt(0);
          if ("b" === r) return {
            type: "message",
            data: P(e.substring(1), t)
          };
          return v[r] ? e.length > 1 ? {
            type: v[r],
            data: e.substring(1)
          } : {
            type: v[r]
          } : m
        },
        A = String.fromCharCode(30);
  
      function w(e) {
        if (e) return function (e) {
          for (var t in w.prototype) e[t] = w.prototype[t];
          return e
        }(e)
      }
      w.prototype.on = w.prototype.addEventListener = function (e, t) {
          return this._callbacks = this._callbacks || {}, (this._callbacks["$" + e] = this._callbacks["$" +
            e] || []).push(t), this
        }, w.prototype.once = function (e, t) {
          function r() {
            this.off(e, r), t.apply(this, arguments)
          }
          return r.fn = t, this.on(e, r), this
        }, w.prototype.off = w.prototype.removeListener = w.prototype.removeAllListeners = w.prototype
        .removeEventListener = function (e, t) {
          if (this._callbacks = this._callbacks || {}, 0 == arguments.length) return this._callbacks = {}, this;
          var r, i = this._callbacks["$" + e];
          if (!i) return this;
          if (1 == arguments.length) return delete this._callbacks["$" + e], this;
          for (var n = 0; n < i.length; n++)
            if ((r = i[n]) === t || r.fn === t) {
              i.splice(n, 1);
              break
            } return 0 === i.length && delete this._callbacks["$" + e], this
        }, w.prototype.emit = function (e) {
          this._callbacks = this._callbacks || {};
          for (var t = new Array(arguments.length - 1), r = this._callbacks["$" + e], i = 1; i < arguments
            .length; i++) t[i - 1] = arguments[i];
          if (r) {
            i = 0;
            for (var n = (r = r.slice(0)).length; i < n; ++i) r[i].apply(this, t)
          }
          return this
        }, w.prototype.emitReserved = w.prototype.emit, w.prototype.listeners = function (e) {
          return this._callbacks = this._callbacks || {}, this._callbacks["$" + e] || []
        }, w.prototype.hasListeners = function (e) {
          return !!this.listeners(e).length
        };
      const k = "undefined" != typeof self ? self : "undefined" != typeof window ? window : Function(
        "return this")();
  
      function N(e, ...t) {
        return t.reduce(((t, r) => (e.hasOwnProperty(r) && (t[r] = e[r]), t)), {})
      }
      const I = k.setTimeout,
        D = k.clearTimeout;
  
      function C(e, t) {
        t.useNativeTimers ? (e.setTimeoutFn = I.bind(k), e.clearTimeoutFn = D.bind(k)) : (e.setTimeoutFn = k
          .setTimeout.bind(k), e.clearTimeoutFn = k.clearTimeout.bind(k))
      }
      class z extends Error {
        constructor(e, t, r) {
          super(e), this.description = t, this.context = r, this.type = "TransportError"
        }
      }
      class x extends w {
        constructor(e) {
          super(), this.writable = !1, C(this, e), this.opts = e, this.query = e.query, this.socket = e.socket
        }
        onError(e, t, r) {
          return super.emitReserved("error", new z(e, t, r)), this
        }
        open() {
          return this.readyState = "opening", this.doOpen(), this
        }
        close() {
          return "opening" !== this.readyState && "open" !== this.readyState || (this.doClose(), this
          .onClose()), this
        }
        send(e) {
          "open" === this.readyState && this.write(e)
        }
        onOpen() {
          this.readyState = "open", this.writable = !0, super.emitReserved("open")
        }
        onData(e) {
          const t = L(e, this.socket.binaryType);
          this.onPacket(t)
        }
        onPacket(e) {
          super.emitReserved("packet", e)
        }
        onClose(e) {
          this.readyState = "closed", super.emitReserved("close", e)
        }
        pause(e) {}
      }
      const E = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_".split(""),
        S = 64,
        O = {};
      let R, Q = 0,
        Y = 0;
  
      function U(e) {
        let t = "";
        do {
          t = E[e % S] + t, e = Math.floor(e / S)
        } while (e > 0);
        return t
      }
  
      function G() {
        const e = U(+new Date);
        return e !== R ? (Q = 0, R = e) : e + "." + U(Q++)
      }
      for (; Y < S; Y++) O[E[Y]] = Y;
  
      function B(e) {
        let t = "";
        for (let r in e) e.hasOwnProperty(r) && (t.length && (t += "&"), t += encodeURIComponent(r) + "=" +
          encodeURIComponent(e[r]));
        return t
      }
      let K = !1;
      try {
        K = "undefined" != typeof XMLHttpRequest && "withCredentials" in new XMLHttpRequest
      } catch (e) {}
      const H = K;
  
      function q(e) {
        const t = e.xdomain;
        try {
          if ("undefined" != typeof XMLHttpRequest && (!t || H)) return new XMLHttpRequest
        } catch (e) {}
        if (!t) try {
          return new(k[["Active"].concat("Object").join("X")])("Microsoft.XMLHTTP")
        } catch (e) {}
      }
  
      function W() {}
      const V = null != new q({
        xdomain: !1
      }).responseType;
      class Z extends w {
        constructor(e, t) {
          super(), C(this, t), this.opts = t, this.method = t.method || "GET", this.uri = e, this.async = !
            1 !== t.async, this.data = void 0 !== t.data ? t.data : null, this.create()
        }
        create() {
          const e = N(this.opts, "agent", "pfx", "key", "passphrase", "cert", "ca", "ciphers",
            "rejectUnauthorized", "autoUnref");
          e.xdomain = !!this.opts.xd, e.xscheme = !!this.opts.xs;
          const t = this.xhr = new q(e);
          try {
            t.open(this.method, this.uri, this.async);
            try {
              if (this.opts.extraHeaders) {
                t.setDisableHeaderCheck && t.setDisableHeaderCheck(!0);
                for (let e in this.opts.extraHeaders) this.opts.extraHeaders.hasOwnProperty(e) && t
                  .setRequestHeader(e, this.opts.extraHeaders[e])
              }
            } catch (e) {}
            if ("POST" === this.method) try {
              t.setRequestHeader("Content-type", "text/plain;charset=UTF-8")
            } catch (e) {}
            try {
              t.setRequestHeader("Accept", "*/*")
            } catch (e) {}
            "withCredentials" in t && (t.withCredentials = this.opts.withCredentials), this.opts
              .requestTimeout && (t.timeout = this.opts.requestTimeout), t.onreadystatechange = () => {
                4 === t.readyState && (200 === t.status || 1223 === t.status ? this.onLoad() : this
                  .setTimeoutFn((() => {
                    this.onError("number" == typeof t.status ? t.status : 0)
                  }), 0))
              }, t.send(this.data)
          } catch (e) {
            return void this.setTimeoutFn((() => {
              this.onError(e)
            }), 0)
          }
          "undefined" != typeof document && (this.index = Z.requestsCount++, Z.requests[this.index] = this)
        }
        onError(e) {
          this.emitReserved("error", e, this.xhr), this.cleanup(!0)
        }
        cleanup(e) {
          if (void 0 !== this.xhr && null !== this.xhr) {
            if (this.xhr.onreadystatechange = W, e) try {
              this.xhr.abort()
            } catch (e) {}
            "undefined" != typeof document && delete Z.requests[this.index], this.xhr = null
          }
        }
        onLoad() {
          const e = this.xhr.responseText;
          null !== e && (this.emitReserved("data", e), this.emitReserved("success"), this.cleanup())
        }
        abort() {
          this.cleanup()
        }
      }
      if (Z.requestsCount = 0, Z.requests = {}, "undefined" != typeof document)
        if ("function" == typeof attachEvent) attachEvent("onunload", F);
        else if ("function" == typeof addEventListener) {
        addEventListener("onpagehide" in k ? "pagehide" : "unload", F, !1)
      }
  
      function F() {
        for (let e in Z.requests) Z.requests.hasOwnProperty(e) && Z.requests[e].abort()
      }
      const J = "function" == typeof Promise && "function" == typeof Promise.resolve ? e => Promise.resolve()
        .then(e) : (e, t) => t(e, 0),
        X = k.WebSocket || k.MozWebSocket,
        _ = "undefined" != typeof navigator && "string" == typeof navigator.product && "reactnative" ===
        navigator.product.toLowerCase();
      const $ = {
          websocket: class extends x {
            constructor(e) {
              super(e), this.supportsBinary = !e.forceBase64
            }
            get name() {
              return "websocket"
            }
            doOpen() {
              if (!this.check()) return;
              const e = this.uri(),
                t = this.opts.protocols,
                r = _ ? {} : N(this.opts, "agent", "perMessageDeflate", "pfx", "key", "passphrase", "cert",
                  "ca", "ciphers", "rejectUnauthorized", "localAddress", "protocolVersion", "origin",
                  "maxPayload", "family", "checkServerIdentity");
              this.opts.extraHeaders && (r.headers = this.opts.extraHeaders);
              try {
                this.ws = _ ? new X(e, t, r) : t ? new X(e, t) : new X(e)
              } catch (e) {
                return this.emitReserved("error", e)
              }
              this.ws.binaryType = this.socket.binaryType || "arraybuffer", this.addEventListeners()
            }
            addEventListeners() {
              this.ws.onopen = () => {
                this.opts.autoUnref && this.ws._socket.unref(), this.onOpen()
              }, this.ws.onclose = e => this.onClose({
                description: "websocket connection closed",
                context: e
              }), this.ws.onmessage = e => this.onData(e.data), this.ws.onerror = e => this.onError(
                "websocket error", e)
            }
            write(e) {
              this.writable = !1;
              for (let t = 0; t < e.length; t++) {
                const r = e[t],
                  i = t === e.length - 1;
                f(r, this.supportsBinary, (e => {
                  try {
                    this.ws.send(e)
                  } catch (e) {}
                  i && J((() => {
                    this.writable = !0, this.emitReserved("drain")
                  }), this.setTimeoutFn)
                }))
              }
            }
            doClose() {
              void 0 !== this.ws && (this.ws.close(), this.ws = null)
            }
            uri() {
              let e = this.query || {};
              const t = this.opts.secure ? "wss" : "ws";
              let r = "";
              this.opts.port && ("wss" === t && 443 !== Number(this.opts.port) || "ws" === t && 80 !==
                Number(this.opts.port)) && (r = ":" + this.opts.port), this.opts.timestampRequests && (e[
                this.opts.timestampParam] = G()), this.supportsBinary || (e.b64 = 1);
              const i = B(e);
              return t + "://" + (-1 !== this.opts.hostname.indexOf(":") ? "[" + this.opts.hostname + "]" :
                this.opts.hostname) + r + this.opts.path + (i.length ? "?" + i : "")
            }
            check() {
              return !!X
            }
          },
          polling: class extends x {
            constructor(e) {
              if (super(e), this.polling = !1, "undefined" != typeof location) {
                const t = "https:" === location.protocol;
                let r = location.port;
                r || (r = t ? "443" : "80"), this.xd = "undefined" != typeof location && e.hostname !==
                  location.hostname || r !== e.port, this.xs = e.secure !== t
              }
              const t = e && e.forceBase64;
              this.supportsBinary = V && !t
            }
            get name() {
              return "polling"
            }
            doOpen() {
              this.poll()
            }
            pause(e) {
              this.readyState = "pausing";
              const t = () => {
                this.readyState = "paused", e()
              };
              if (this.polling || !this.writable) {
                let e = 0;
                this.polling && (e++, this.once("pollComplete", (function () {
                  --e || t()
                }))), this.writable || (e++, this.once("drain", (function () {
                  --e || t()
                })))
              } else t()
            }
            poll() {
              this.polling = !0, this.doPoll(), this.emitReserved("poll")
            }
            onData(e) {
              ((e, t) => {
                const r = e.split(A),
                  i = [];
                for (let e = 0; e < r.length; e++) {
                  const n = L(r[e], t);
                  if (i.push(n), "error" === n.type) break
                }
                return i
              })(e, this.socket.binaryType).forEach((e => {
                if ("opening" === this.readyState && "open" === e.type && this.onOpen(), "close" === e
                  .type) return this.onClose({
                  description: "transport closed by the server"
                }), !1;
                this.onPacket(e)
              })), "closed" !== this.readyState && (this.polling = !1, this.emitReserved("pollComplete"),
                "open" === this.readyState && this.poll())
            }
            doClose() {
              const e = () => {
                this.write([{
                  type: "close"
                }])
              };
              "open" === this.readyState ? e() : this.once("open", e)
            }
            write(e) {
              this.writable = !1, ((e, t) => {
                const r = e.length,
                  i = new Array(r);
                let n = 0;
                e.forEach(((e, o) => {
                  f(e, !1, (e => {
                    i[o] = e, ++n === r && t(i.join(A))
                  }))
                }))
              })(e, (e => {
                this.doWrite(e, (() => {
                  this.writable = !0, this.emitReserved("drain")
                }))
              }))
            }
            uri() {
              let e = this.query || {};
              const t = this.opts.secure ? "https" : "http";
              let r = "";
              !1 !== this.opts.timestampRequests && (e[this.opts.timestampParam] = G()), this
                .supportsBinary || e.sid || (e.b64 = 1), this.opts.port && ("https" === t && 443 !== Number(
                  this.opts.port) || "http" === t && 80 !== Number(this.opts.port)) && (r = ":" + this.opts
                  .port);
              const i = B(e);
              return t + "://" + (-1 !== this.opts.hostname.indexOf(":") ? "[" + this.opts.hostname + "]" :
                this.opts.hostname) + r + this.opts.path + (i.length ? "?" + i : "")
            }
            request(e = {}) {
              return Object.assign(e, {
                xd: this.xd,
                xs: this.xs
              }, this.opts), new Z(this.uri(), e)
            }
            doWrite(e, t) {
              const r = this.request({
                method: "POST",
                data: e
              });
              r.on("success", t), r.on("error", ((e, t) => {
                this.onError("xhr post error", e, t)
              }))
            }
            doPoll() {
              const e = this.request();
              e.on("data", this.onData.bind(this)), e.on("error", ((e, t) => {
                this.onError("xhr poll error", e, t)
              })), this.pollXhr = e
            }
          }
        },
        ee =
        /^(?:(?![^:@\/?#]+:[^:@\/]*@)(http|https|ws|wss):\/\/)?((?:(([^:@\/?#]*)(?::([^:@\/?#]*))?)?@)?((?:[a-f0-9]{0,4}:){2,7}[a-f0-9]{0,4}|[^:\/?#]*)(?::(\d*))?)(((\/(?:[^?#](?![^?#\/]*\.[^?#\/.]+(?:[?#]|$)))*\/?)?([^?#\/]*))(?:\?([^#]*))?(?:#(.*))?)/,
        te = ["source", "protocol", "authority", "userInfo", "user", "password", "host", "port", "relative",
          "path", "directory", "file", "query", "anchor"
        ];
  
      function re(e) {
        const t = e,
          r = e.indexOf("["),
          i = e.indexOf("]"); - 1 != r && -1 != i && (e = e.substring(0, r) + e.substring(r, i).replace(/:/g,
          ";") + e.substring(i, e.length));
        let n = ee.exec(e || ""),
          o = {},
          a = 14;
        for (; a--;) o[te[a]] = n[a] || "";
        return -1 != r && -1 != i && (o.source = t, o.host = o.host.substring(1, o.host.length - 1).replace(
            /;/g, ":"), o.authority = o.authority.replace("[", "").replace("]", "").replace(/;/g, ":"), o
          .ipv6uri = !0), o.pathNames = function (e, t) {
          const r = /\/{2,9}/g,
            i = t.replace(r, "/").split("/");
          "/" != t.slice(0, 1) && 0 !== t.length || i.splice(0, 1);
          "/" == t.slice(-1) && i.splice(i.length - 1, 1);
          return i
        }(0, o.path), o.queryKey = function (e, t) {
          const r = {};
          return t.replace(/(?:^|&)([^&=]*)=?([^&]*)/g, (function (e, t, i) {
            t && (r[t] = i)
          })), r
        }(0, o.query), o
      }
      class ie extends w {
        constructor(e, t = {}) {
          super(), this.writeBuffer = [], e && "object" == typeof e && (t = e, e = null), e ? (e = re(e), t
              .hostname = e.host, t.secure = "https" === e.protocol || "wss" === e.protocol, t.port = e.port,
              e.query && (t.query = e.query)) : t.host && (t.hostname = re(t.host).host), C(this, t), this
            .secure = null != t.secure ? t.secure : "undefined" != typeof location && "https:" === location
            .protocol, t.hostname && !t.port && (t.port = this.secure ? "443" : "80"), this.hostname = t
            .hostname || ("undefined" != typeof location ? location.hostname : "localhost"), this.port = t
            .port || ("undefined" != typeof location && location.port ? location.port : this.secure ? "443" :
              "80"), this.transports = t.transports || ["polling", "websocket"], this.writeBuffer = [], this
            .prevBufferLen = 0, this.opts = Object.assign({
              path: "/engine.io",
              agent: !1,
              withCredentials: !1,
              upgrade: !0,
              timestampParam: "t",
              rememberUpgrade: !1,
              addTrailingSlash: !0,
              rejectUnauthorized: !0,
              perMessageDeflate: {
                threshold: 1024
              },
              transportOptions: {},
              closeOnBeforeunload: !0
            }, t), this.opts.path = this.opts.path.replace(/\/$/, "") + (this.opts.addTrailingSlash ? "/" :
              ""), "string" == typeof this.opts.query && (this.opts.query = function (e) {
              let t = {},
                r = e.split("&");
              for (let e = 0, i = r.length; e < i; e++) {
                let i = r[e].split("=");
                t[decodeURIComponent(i[0])] = decodeURIComponent(i[1])
              }
              return t
            }(this.opts.query)), this.id = null, this.upgrades = null, this.pingInterval = null, this
            .pingTimeout = null, this.pingTimeoutTimer = null, "function" == typeof addEventListener && (this
              .opts.closeOnBeforeunload && (this.beforeunloadEventListener = () => {
                this.transport && (this.transport.removeAllListeners(), this.transport.close())
              }, addEventListener("beforeunload", this.beforeunloadEventListener, !1)), "localhost" !== this
              .hostname && (this.offlineEventListener = () => {
                this.onClose("transport close", {
                  description: "network connection lost"
                })
              }, addEventListener("offline", this.offlineEventListener, !1))), this.open()
        }
        createTransport(e) {
          const t = Object.assign({}, this.opts.query);
          t.EIO = 4, t.transport = e, this.id && (t.sid = this.id);
          const r = Object.assign({}, this.opts.transportOptions[e], this.opts, {
            query: t,
            socket: this,
            hostname: this.hostname,
            secure: this.secure,
            port: this.port
          });
          return new $[e](r)
        }
        open() {
          let e;
          if (this.opts.rememberUpgrade && ie.priorWebsocketSuccess && -1 !== this.transports.indexOf(
              "websocket")) e = "websocket";
          else {
            if (0 === this.transports.length) return void this.setTimeoutFn((() => {
              this.emitReserved("error", "No transports available")
            }), 0);
            e = this.transports[0]
          }
          this.readyState = "opening";
          try {
            e = this.createTransport(e)
          } catch (e) {
            return this.transports.shift(), void this.open()
          }
          e.open(), this.setTransport(e)
        }
        setTransport(e) {
          this.transport && this.transport.removeAllListeners(), this.transport = e, e.on("drain", this
              .onDrain.bind(this)).on("packet", this.onPacket.bind(this)).on("error", this.onError.bind(this))
            .on("close", (e => this.onClose("transport close", e)))
        }
        probe(e) {
          let t = this.createTransport(e),
            r = !1;
          ie.priorWebsocketSuccess = !1;
          const i = () => {
            r || (t.send([{
              type: "ping",
              data: "probe"
            }]), t.once("packet", (e => {
              if (!r)
                if ("pong" === e.type && "probe" === e.data) {
                  if (this.upgrading = !0, this.emitReserved("upgrading", t), !t) return;
                  ie.priorWebsocketSuccess = "websocket" === t.name, this.transport.pause((() => {
                    r || "closed" !== this.readyState && (l(), this.setTransport(t), t.send([{
                        type: "upgrade"
                      }]), this.emitReserved("upgrade", t), t = null, this.upgrading = !1,
                      this.flush())
                  }))
                } else {
                  const e = new Error("probe error");
                  e.transport = t.name, this.emitReserved("upgradeError", e)
                }
            })))
          };
  
          function n() {
            r || (r = !0, l(), t.close(), t = null)
          }
          const o = e => {
            const r = new Error("probe error: " + e);
            r.transport = t.name, n(), this.emitReserved("upgradeError", r)
          };
  
          function a() {
            o("transport closed")
          }
  
          function s() {
            o("socket closed")
          }
  
          function c(e) {
            t && e.name !== t.name && n()
          }
          const l = () => {
            t.removeListener("open", i), t.removeListener("error", o), t.removeListener("close", a), this
              .off("close", s), this.off("upgrading", c)
          };
          t.once("open", i), t.once("error", o), t.once("close", a), this.once("close", s), this.once(
            "upgrading", c), t.open()
        }
        onOpen() {
          if (this.readyState = "open", ie.priorWebsocketSuccess = "websocket" === this.transport.name, this
            .emitReserved("open"), this.flush(), "open" === this.readyState && this.opts.upgrade) {
            let e = 0;
            const t = this.upgrades.length;
            for (; e < t; e++) this.probe(this.upgrades[e])
          }
        }
        onPacket(e) {
          if ("opening" === this.readyState || "open" === this.readyState || "closing" === this.readyState)
            switch (this.emitReserved("packet", e), this.emitReserved("heartbeat"), e.type) {
            case "open":
              this.onHandshake(JSON.parse(e.data));
              break;
            case "ping":
              this.resetPingTimeout(), this.sendPacket("pong"), this.emitReserved("ping"), this.emitReserved(
                "pong");
              break;
            case "error":
              const t = new Error("server error");
              t.code = e.data, this.onError(t);
              break;
            case "message":
              this.emitReserved("data", e.data), this.emitReserved("message", e.data)
            }
        }
        onHandshake(e) {
          this.emitReserved("handshake", e), this.id = e.sid, this.transport.query.sid = e.sid, this
            .upgrades = this.filterUpgrades(e.upgrades), this.pingInterval = e.pingInterval, this
            .pingTimeout = e.pingTimeout, this.maxPayload = e.maxPayload, this.onOpen(), "closed" !== this
            .readyState && this.resetPingTimeout()
        }
        resetPingTimeout() {
          this.clearTimeoutFn(this.pingTimeoutTimer), this.pingTimeoutTimer = this.setTimeoutFn((() => {
            this.onClose("ping timeout")
          }), this.pingInterval + this.pingTimeout), this.opts.autoUnref && this.pingTimeoutTimer.unref()
        }
        onDrain() {
          this.writeBuffer.splice(0, this.prevBufferLen), this.prevBufferLen = 0, 0 === this.writeBuffer
            .length ? this.emitReserved("drain") : this.flush()
        }
        flush() {
          if ("closed" !== this.readyState && this.transport.writable && !this.upgrading && this.writeBuffer
            .length) {
            const e = this.getWritablePackets();
            this.transport.send(e), this.prevBufferLen = e.length, this.emitReserved("flush")
          }
        }
        getWritablePackets() {
          if (!(this.maxPayload && "polling" === this.transport.name && this.writeBuffer.length > 1))
          return this.writeBuffer;
          let e = 1;
          for (let r = 0; r < this.writeBuffer.length; r++) {
            const i = this.writeBuffer[r].data;
            if (i && (e += "string" == typeof (t = i) ? function (e) {
                let t = 0,
                  r = 0;
                for (let i = 0, n = e.length; i < n; i++) t = e.charCodeAt(i), t < 128 ? r += 1 : t < 2048 ?
                  r += 2 : t < 55296 || t >= 57344 ? r += 3 : (i++, r += 4);
                return r
              }(t) : Math.ceil(1.33 * (t.byteLength || t.size))), r > 0 && e > this.maxPayload) return this
              .writeBuffer.slice(0, r);
            e += 2
          }
          var t;
          return this.writeBuffer
        }
        write(e, t, r) {
          return this.sendPacket("message", e, t, r), this
        }
        send(e, t, r) {
          return this.sendPacket("message", e, t, r), this
        }
        sendPacket(e, t, r, i) {
          if ("function" == typeof t && (i = t, t = void 0), "function" == typeof r && (i = r, r = null),
            "closing" === this.readyState || "closed" === this.readyState) return;
          (r = r || {}).compress = !1 !== r.compress;
          const n = {
            type: e,
            data: t,
            options: r
          };
          this.emitReserved("packetCreate", n), this.writeBuffer.push(n), i && this.once("flush", i), this
            .flush()
        }
        close() {
          const e = () => {
              this.onClose("forced close"), this.transport.close()
            },
            t = () => {
              this.off("upgrade", t), this.off("upgradeError", t), e()
            },
            r = () => {
              this.once("upgrade", t), this.once("upgradeError", t)
            };
          return "opening" !== this.readyState && "open" !== this.readyState || (this.readyState = "closing",
            this.writeBuffer.length ? this.once("drain", (() => {
              this.upgrading ? r() : e()
            })) : this.upgrading ? r() : e()), this
        }
        onError(e) {
          ie.priorWebsocketSuccess = !1, this.emitReserved("error", e), this.onClose("transport error", e)
        }
        onClose(e, t) {
          "opening" !== this.readyState && "open" !== this.readyState && "closing" !== this.readyState || (
            this.clearTimeoutFn(this.pingTimeoutTimer), this.transport.removeAllListeners("close"), this
            .transport.close(), this.transport.removeAllListeners(), "function" ==
            typeof removeEventListener && (removeEventListener("beforeunload", this
              .beforeunloadEventListener, !1), removeEventListener("offline", this.offlineEventListener, !
              1)), this.readyState = "closed", this.id = null, this.emitReserved("close", e, t), this
            .writeBuffer = [], this.prevBufferLen = 0)
        }
        filterUpgrades(e) {
          const t = [];
          let r = 0;
          const i = e.length;
          for (; r < i; r++) ~this.transports.indexOf(e[r]) && t.push(e[r]);
          return t
        }
      }
      ie.protocol = 4;
      ie.protocol;
      const ne = "function" == typeof ArrayBuffer,
        oe = e => "function" == typeof ArrayBuffer.isView ? ArrayBuffer.isView(e) : e
        .buffer instanceof ArrayBuffer,
        ae = Object.prototype.toString,
        se = "function" == typeof Blob || "undefined" != typeof Blob && "[object BlobConstructor]" === ae.call(
          Blob),
        ce = "function" == typeof File || "undefined" != typeof File && "[object FileConstructor]" === ae.call(
          File);
  
      function le(e) {
        return ne && (e instanceof ArrayBuffer || oe(e)) || se && e instanceof Blob || ce && e instanceof File
      }
  
      function de(e, t) {
        if (!e || "object" != typeof e) return !1;
        if (Array.isArray(e)) {
          for (let t = 0, r = e.length; t < r; t++)
            if (de(e[t])) return !0;
          return !1
        }
        if (le(e)) return !0;
        if (e.toJSON && "function" == typeof e.toJSON && 1 === arguments.length) return de(e.toJSON(), !0);
        for (const t in e)
          if (Object.prototype.hasOwnProperty.call(e, t) && de(e[t])) return !0;
        return !1
      }
  
      function ue(e) {
        const t = [],
          r = e.data,
          i = e;
        return i.data = pe(r, t), i.attachments = t.length, {
          packet: i,
          buffers: t
        }
      }
  
      function pe(e, t) {
        if (!e) return e;
        if (le(e)) {
          const r = {
            _placeholder: !0,
            num: t.length
          };
          return t.push(e), r
        }
        if (Array.isArray(e)) {
          const r = new Array(e.length);
          for (let i = 0; i < e.length; i++) r[i] = pe(e[i], t);
          return r
        }
        if ("object" == typeof e && !(e instanceof Date)) {
          const r = {};
          for (const i in e) Object.prototype.hasOwnProperty.call(e, i) && (r[i] = pe(e[i], t));
          return r
        }
        return e
      }
  
      function ve(e, t) {
        return e.data = me(e.data, t), e.attachments = void 0, e
      }
  
      function me(e, t) {
        if (!e) return e;
        if (e && !0 === e._placeholder) {
          if ("number" == typeof e.num && e.num >= 0 && e.num < t.length) return t[e.num];
          throw new Error("illegal attachments")
        }
        if (Array.isArray(e))
          for (let r = 0; r < e.length; r++) e[r] = me(e[r], t);
        else if ("object" == typeof e)
          for (const r in e) Object.prototype.hasOwnProperty.call(e, r) && (e[r] = me(e[r], t));
        return e
      }
      const he = 5;
      var ge;
      ! function (e) {
        e[e.CONNECT = 0] = "CONNECT", e[e.DISCONNECT = 1] = "DISCONNECT", e[e.EVENT = 2] = "EVENT", e[e.ACK =
          3] = "ACK", e[e.CONNECT_ERROR = 4] = "CONNECT_ERROR", e[e.BINARY_EVENT = 5] = "BINARY_EVENT", e[e
            .BINARY_ACK = 6] = "BINARY_ACK"
      }(ge || (ge = {}));
      class be {
        constructor(e) {
          this.replacer = e
        }
        encode(e) {
          return e.type !== ge.EVENT && e.type !== ge.ACK || !de(e) ? [this.encodeAsString(e)] : (e.type = e
            .type === ge.EVENT ? ge.BINARY_EVENT : ge.BINARY_ACK, this.encodeAsBinary(e))
        }
        encodeAsString(e) {
          let t = "" + e.type;
          return e.type !== ge.BINARY_EVENT && e.type !== ge.BINARY_ACK || (t += e.attachments + "-"), e
            .nsp && "/" !== e.nsp && (t += e.nsp + ","), null != e.id && (t += e.id), null != e.data && (t +=
              JSON.stringify(e.data, this.replacer)), t
        }
        encodeAsBinary(e) {
          const t = ue(e),
            r = this.encodeAsString(t.packet),
            i = t.buffers;
          return i.unshift(r), i
        }
      }
      class fe extends w {
        constructor(e) {
          super(), this.reviver = e
        }
        add(e) {
          let t;
          if ("string" == typeof e) {
            if (this.reconstructor) throw new Error("got plaintext data when reconstructing a packet");
            t = this.decodeString(e), t.type === ge.BINARY_EVENT || t.type === ge.BINARY_ACK ? (this
                .reconstructor = new ye(t), 0 === t.attachments && super.emitReserved("decoded", t)) : super
              .emitReserved("decoded", t)
          } else {
            if (!le(e) && !e.base64) throw new Error("Unknown type: " + e);
            if (!this.reconstructor) throw new Error("got binary data when not reconstructing a packet");
            t = this.reconstructor.takeBinaryData(e), t && (this.reconstructor = null, super.emitReserved(
              "decoded", t))
          }
        }
        decodeString(e) {
          let t = 0;
          const r = {
            type: Number(e.charAt(0))
          };
          if (void 0 === ge[r.type]) throw new Error("unknown packet type " + r.type);
          if (r.type === ge.BINARY_EVENT || r.type === ge.BINARY_ACK) {
            const i = t + 1;
            for (;
              "-" !== e.charAt(++t) && t != e.length;);
            const n = e.substring(i, t);
            if (n != Number(n) || "-" !== e.charAt(t)) throw new Error("Illegal attachments");
            r.attachments = Number(n)
          }
          if ("/" === e.charAt(t + 1)) {
            const i = t + 1;
            for (; ++t;) {
              if ("," === e.charAt(t)) break;
              if (t === e.length) break
            }
            r.nsp = e.substring(i, t)
          } else r.nsp = "/";
          const i = e.charAt(t + 1);
          if ("" !== i && Number(i) == i) {
            const i = t + 1;
            for (; ++t;) {
              const r = e.charAt(t);
              if (null == r || Number(r) != r) {
                --t;
                break
              }
              if (t === e.length) break
            }
            r.id = Number(e.substring(i, t + 1))
          }
          if (e.charAt(++t)) {
            const i = this.tryParse(e.substr(t));
            if (!fe.isPayloadValid(r.type, i)) throw new Error("invalid payload");
            r.data = i
          }
          return r
        }
        tryParse(e) {
          try {
            return JSON.parse(e, this.reviver)
          } catch (e) {
            return !1
          }
        }
        static isPayloadValid(e, t) {
          switch (e) {
          case ge.CONNECT:
            return "object" == typeof t;
          case ge.DISCONNECT:
            return void 0 === t;
          case ge.CONNECT_ERROR:
            return "string" == typeof t || "object" == typeof t;
          case ge.EVENT:
          case ge.BINARY_EVENT:
            return Array.isArray(t) && t.length > 0;
          case ge.ACK:
          case ge.BINARY_ACK:
            return Array.isArray(t)
          }
        }
        destroy() {
          this.reconstructor && this.reconstructor.finishedReconstruction()
        }
      }
      class ye {
        constructor(e) {
          this.packet = e, this.buffers = [], this.reconPack = e
        }
        takeBinaryData(e) {
          if (this.buffers.push(e), this.buffers.length === this.reconPack.attachments) {
            const e = ve(this.reconPack, this.buffers);
            return this.finishedReconstruction(), e
          }
          return null
        }
        finishedReconstruction() {
          this.reconPack = null, this.buffers = []
        }
      }
  
      function Me(e, t, r) {
        return e.on(t, r),
          function () {
            e.off(t, r)
          }
      }
      const je = Object.freeze({
        connect: 1,
        connect_error: 1,
        disconnect: 1,
        disconnecting: 1,
        newListener: 1,
        removeListener: 1
      });
      class Pe extends w {
        constructor(e, t, r) {
          super(), this.connected = !1, this.recovered = !1, this.receiveBuffer = [], this.sendBuffer = [],
            this._queue = [], this._queueSeq = 0, this.ids = 0, this.acks = {}, this.flags = {}, this.io = e,
            this.nsp = t, r && r.auth && (this.auth = r.auth), this._opts = Object.assign({}, r), this.io
            ._autoConnect && this.open()
        }
        get disconnected() {
          return !this.connected
        }
        subEvents() {
          if (this.subs) return;
          const e = this.io;
          this.subs = [Me(e, "open", this.onopen.bind(this)), Me(e, "packet", this.onpacket.bind(this)), Me(e,
            "error", this.onerror.bind(this)), Me(e, "close", this.onclose.bind(this))]
        }
        get active() {
          return !!this.subs
        }
        connect() {
          return this.connected || (this.subEvents(), this.io._reconnecting || this.io.open(), "open" === this
            .io._readyState && this.onopen()), this
        }
        open() {
          return this.connect()
        }
        send(...e) {
          return e.unshift("message"), this.emit.apply(this, e), this
        }
        emit(e, ...t) {
          if (je.hasOwnProperty(e)) throw new Error('"' + e.toString() + '" is a reserved event name');
          if (t.unshift(e), this._opts.retries && !this.flags.fromQueue && !this.flags.volatile) return this
            ._addToQueue(t), this;
          const r = {
            type: ge.EVENT,
            data: t,
            options: {}
          };
          if (r.options.compress = !1 !== this.flags.compress, "function" == typeof t[t.length - 1]) {
            const e = this.ids++,
              i = t.pop();
            this._registerAckCallback(e, i), r.id = e
          }
          const i = this.io.engine && this.io.engine.transport && this.io.engine.transport.writable;
          return this.flags.volatile && (!i || !this.connected) || (this.connected ? (this
            .notifyOutgoingListeners(r), this.packet(r)) : this.sendBuffer.push(r)), this.flags = {}, this
        }
        _registerAckCallback(e, t) {
          var r;
          const i = null !== (r = this.flags.timeout) && void 0 !== r ? r : this._opts.ackTimeout;
          if (void 0 === i) return void(this.acks[e] = t);
          const n = this.io.setTimeoutFn((() => {
            delete this.acks[e];
            for (let t = 0; t < this.sendBuffer.length; t++) this.sendBuffer[t].id === e && this
              .sendBuffer.splice(t, 1);
            t.call(this, new Error("operation has timed out"))
          }), i);
          this.acks[e] = (...e) => {
            this.io.clearTimeoutFn(n), t.apply(this, [null, ...e])
          }
        }
        emitWithAck(e, ...t) {
          const r = void 0 !== this.flags.timeout || void 0 !== this._opts.ackTimeout;
          return new Promise(((i, n) => {
            t.push(((e, t) => r ? e ? n(e) : i(t) : i(e))), this.emit(e, ...t)
          }))
        }
        _addToQueue(e) {
          let t;
          "function" == typeof e[e.length - 1] && (t = e.pop());
          const r = {
            id: this._queueSeq++,
            tryCount: 0,
            pending: !1,
            args: e,
            flags: Object.assign({
              fromQueue: !0
            }, this.flags)
          };
          e.push(((e, ...i) => {
            if (r !== this._queue[0]) return;
            return null !== e ? r.tryCount > this._opts.retries && (this._queue.shift(), t && t(e)) : (
              this._queue.shift(), t && t(null, ...i)), r.pending = !1, this._drainQueue()
          })), this._queue.push(r), this._drainQueue()
        }
        _drainQueue(e = !1) {
          if (!this.connected || 0 === this._queue.length) return;
          const t = this._queue[0];
          t.pending && !e || (t.pending = !0, t.tryCount++, this.flags = t.flags, this.emit.apply(this, t
            .args))
        }
        packet(e) {
          e.nsp = this.nsp, this.io._packet(e)
        }
        onopen() {
          "function" == typeof this.auth ? this.auth((e => {
            this._sendConnectPacket(e)
          })) : this._sendConnectPacket(this.auth)
        }
        _sendConnectPacket(e) {
          this.packet({
            type: ge.CONNECT,
            data: this._pid ? Object.assign({
              pid: this._pid,
              offset: this._lastOffset
            }, e) : e
          })
        }
        onerror(e) {
          this.connected || this.emitReserved("connect_error", e)
        }
        onclose(e, t) {
          this.connected = !1, delete this.id, this.emitReserved("disconnect", e, t)
        }
        onpacket(e) {
          if (e.nsp === this.nsp) switch (e.type) {
          case ge.CONNECT:
            e.data && e.data.sid ? this.onconnect(e.data.sid, e.data.pid) : this.emitReserved(
              "connect_error", new Error(
                "It seems you are trying to reach a Socket.IO server in v2.x with a v3.x client, but they are not compatible (more information here: https://socket.io/docs/v3/migrating-from-2-x-to-3-0/)"
                ));
            break;
          case ge.EVENT:
          case ge.BINARY_EVENT:
            this.onevent(e);
            break;
          case ge.ACK:
          case ge.BINARY_ACK:
            this.onack(e);
            break;
          case ge.DISCONNECT:
            this.ondisconnect();
            break;
          case ge.CONNECT_ERROR:
            this.destroy();
            const t = new Error(e.data.message);
            t.data = e.data.data, this.emitReserved("connect_error", t)
          }
        }
        onevent(e) {
          const t = e.data || [];
          null != e.id && t.push(this.ack(e.id)), this.connected ? this.emitEvent(t) : this.receiveBuffer
            .push(Object.freeze(t))
        }
        emitEvent(e) {
          if (this._anyListeners && this._anyListeners.length) {
            const t = this._anyListeners.slice();
            for (const r of t) r.apply(this, e)
          }
          super.emit.apply(this, e), this._pid && e.length && "string" == typeof e[e.length - 1] && (this
            ._lastOffset = e[e.length - 1])
        }
        ack(e) {
          const t = this;
          let r = !1;
          return function (...i) {
            r || (r = !0, t.packet({
              type: ge.ACK,
              id: e,
              data: i
            }))
          }
        }
        onack(e) {
          const t = this.acks[e.id];
          "function" == typeof t && (t.apply(this, e.data), delete this.acks[e.id])
        }
        onconnect(e, t) {
          this.id = e, this.recovered = t && this._pid === t, this._pid = t, this.connected = !0, this
            .emitBuffered(), this.emitReserved("connect"), this._drainQueue(!0)
        }
        emitBuffered() {
          this.receiveBuffer.forEach((e => this.emitEvent(e))), this.receiveBuffer = [], this.sendBuffer
            .forEach((e => {
              this.notifyOutgoingListeners(e), this.packet(e)
            })), this.sendBuffer = []
        }
        ondisconnect() {
          this.destroy(), this.onclose("io server disconnect")
        }
        destroy() {
          this.subs && (this.subs.forEach((e => e())), this.subs = void 0), this.io._destroy(this)
        }
        disconnect() {
          return this.connected && this.packet({
            type: ge.DISCONNECT
          }), this.destroy(), this.connected && this.onclose("io client disconnect"), this
        }
        close() {
          return this.disconnect()
        }
        compress(e) {
          return this.flags.compress = e, this
        }
        get volatile() {
          return this.flags.volatile = !0, this
        }
        timeout(e) {
          return this.flags.timeout = e, this
        }
        onAny(e) {
          return this._anyListeners = this._anyListeners || [], this._anyListeners.push(e), this
        }
        prependAny(e) {
          return this._anyListeners = this._anyListeners || [], this._anyListeners.unshift(e), this
        }
        offAny(e) {
          if (!this._anyListeners) return this;
          if (e) {
            const t = this._anyListeners;
            for (let r = 0; r < t.length; r++)
              if (e === t[r]) return t.splice(r, 1), this
          } else this._anyListeners = [];
          return this
        }
        listenersAny() {
          return this._anyListeners || []
        }
        onAnyOutgoing(e) {
          return this._anyOutgoingListeners = this._anyOutgoingListeners || [], this._anyOutgoingListeners
            .push(e), this
        }
        prependAnyOutgoing(e) {
          return this._anyOutgoingListeners = this._anyOutgoingListeners || [], this._anyOutgoingListeners
            .unshift(e), this
        }
        offAnyOutgoing(e) {
          if (!this._anyOutgoingListeners) return this;
          if (e) {
            const t = this._anyOutgoingListeners;
            for (let r = 0; r < t.length; r++)
              if (e === t[r]) return t.splice(r, 1), this
          } else this._anyOutgoingListeners = [];
          return this
        }
        listenersAnyOutgoing() {
          return this._anyOutgoingListeners || []
        }
        notifyOutgoingListeners(e) {
          if (this._anyOutgoingListeners && this._anyOutgoingListeners.length) {
            const t = this._anyOutgoingListeners.slice();
            for (const r of t) r.apply(this, e.data)
          }
        }
      }
  
      function Te(e) {
        e = e || {}, this.ms = e.min || 100, this.max = e.max || 1e4, this.factor = e.factor || 2, this.jitter =
          e.jitter > 0 && e.jitter <= 1 ? e.jitter : 0, this.attempts = 0
      }
      Te.prototype.duration = function () {
        var e = this.ms * Math.pow(this.factor, this.attempts++);
        if (this.jitter) {
          var t = Math.random(),
            r = Math.floor(t * this.jitter * e);
          e = 0 == (1 & Math.floor(10 * t)) ? e - r : e + r
        }
        return 0 | Math.min(e, this.max)
      }, Te.prototype.reset = function () {
        this.attempts = 0
      }, Te.prototype.setMin = function (e) {
        this.ms = e
      }, Te.prototype.setMax = function (e) {
        this.max = e
      }, Te.prototype.setJitter = function (e) {
        this.jitter = e
      };
      class Le extends w {
        constructor(t, r) {
          var i;
          super(), this.nsps = {}, this.subs = [], t && "object" == typeof t && (r = t, t = void 0), (r = r ||
            {}).path = r.path || "/socket.io", this.opts = r, C(this, r), this.reconnection(!1 !== r
              .reconnection), this.reconnectionAttempts(r.reconnectionAttempts || 1 / 0), this
            .reconnectionDelay(r.reconnectionDelay || 1e3), this.reconnectionDelayMax(r
              .reconnectionDelayMax || 5e3), this.randomizationFactor(null !== (i = r.randomizationFactor) &&
              void 0 !== i ? i : .5), this.backoff = new Te({
              min: this.reconnectionDelay(),
              max: this.reconnectionDelayMax(),
              jitter: this.randomizationFactor()
            }), this.timeout(null == r.timeout ? 2e4 : r.timeout), this._readyState = "closed", this.uri = t;
          const n = r.parser || e;
          this.encoder = new n.Encoder, this.decoder = new n.Decoder, this._autoConnect = !1 !== r
            .autoConnect, this._autoConnect && this.open()
        }
        reconnection(e) {
          return arguments.length ? (this._reconnection = !!e, this) : this._reconnection
        }
        reconnectionAttempts(e) {
          return void 0 === e ? this._reconnectionAttempts : (this._reconnectionAttempts = e, this)
        }
        reconnectionDelay(e) {
          var t;
          return void 0 === e ? this._reconnectionDelay : (this._reconnectionDelay = e, null === (t = this
            .backoff) || void 0 === t || t.setMin(e), this)
        }
        randomizationFactor(e) {
          var t;
          return void 0 === e ? this._randomizationFactor : (this._randomizationFactor = e, null === (t = this
            .backoff) || void 0 === t || t.setJitter(e), this)
        }
        reconnectionDelayMax(e) {
          var t;
          return void 0 === e ? this._reconnectionDelayMax : (this._reconnectionDelayMax = e, null === (t =
            this.backoff) || void 0 === t || t.setMax(e), this)
        }
        timeout(e) {
          return arguments.length ? (this._timeout = e, this) : this._timeout
        }
        maybeReconnectOnOpen() {
          !this._reconnecting && this._reconnection && 0 === this.backoff.attempts && this.reconnect()
        }
        open(e) {
          if (~this._readyState.indexOf("open")) return this;
          this.engine = new ie(this.uri, this.opts);
          const t = this.engine,
            r = this;
          this._readyState = "opening", this.skipReconnect = !1;
          const i = Me(t, "open", (function () {
              r.onopen(), e && e()
            })),
            n = Me(t, "error", (t => {
              r.cleanup(), r._readyState = "closed", this.emitReserved("error", t), e ? e(t) : r
                .maybeReconnectOnOpen()
            }));
          if (!1 !== this._timeout) {
            const e = this._timeout;
            0 === e && i();
            const r = this.setTimeoutFn((() => {
              i(), t.close(), t.emit("error", new Error("timeout"))
            }), e);
            this.opts.autoUnref && r.unref(), this.subs.push((function () {
              clearTimeout(r)
            }))
          }
          return this.subs.push(i), this.subs.push(n), this
        }
        connect(e) {
          return this.open(e)
        }
        onopen() {
          this.cleanup(), this._readyState = "open", this.emitReserved("open");
          const e = this.engine;
          this.subs.push(Me(e, "ping", this.onping.bind(this)), Me(e, "data", this.ondata.bind(this)), Me(e,
            "error", this.onerror.bind(this)), Me(e, "close", this.onclose.bind(this)), Me(this.decoder,
            "decoded", this.ondecoded.bind(this)))
        }
        onping() {
          this.emitReserved("ping")
        }
        ondata(e) {
          try {
            this.decoder.add(e)
          } catch (e) {
            this.onclose("parse error", e)
          }
        }
        ondecoded(e) {
          J((() => {
            this.emitReserved("packet", e)
          }), this.setTimeoutFn)
        }
        onerror(e) {
          this.emitReserved("error", e)
        }
        socket(e, t) {
          let r = this.nsps[e];
          return r ? this._autoConnect && !r.active && r.connect() : (r = new Pe(this, e, t), this.nsps[e] =
            r), r
        }
        _destroy(e) {
          const t = Object.keys(this.nsps);
          for (const e of t) {
            if (this.nsps[e].active) return
          }
          this._close()
        }
        _packet(e) {
          const t = this.encoder.encode(e);
          for (let r = 0; r < t.length; r++) this.engine.write(t[r], e.options)
        }
        cleanup() {
          this.subs.forEach((e => e())), this.subs.length = 0, this.decoder.destroy()
        }
        _close() {
          this.skipReconnect = !0, this._reconnecting = !1, this.onclose("forced close"), this.engine && this
            .engine.close()
        }
        disconnect() {
          return this._close()
        }
        onclose(e, t) {
          this.cleanup(), this.backoff.reset(), this._readyState = "closed", this.emitReserved("close", e, t),
            this._reconnection && !this.skipReconnect && this.reconnect()
        }
        reconnect() {
          if (this._reconnecting || this.skipReconnect) return this;
          const e = this;
          if (this.backoff.attempts >= this._reconnectionAttempts) this.backoff.reset(), this.emitReserved(
            "reconnect_failed"), this._reconnecting = !1;
          else {
            const t = this.backoff.duration();
            this._reconnecting = !0;
            const r = this.setTimeoutFn((() => {
              e.skipReconnect || (this.emitReserved("reconnect_attempt", e.backoff.attempts), e
                .skipReconnect || e.open((t => {
                  t ? (e._reconnecting = !1, e.reconnect(), this.emitReserved("reconnect_error",
                    t)) : e.onreconnect()
                })))
            }), t);
            this.opts.autoUnref && r.unref(), this.subs.push((function () {
              clearTimeout(r)
            }))
          }
        }
        onreconnect() {
          const e = this.backoff.attempts;
          this._reconnecting = !1, this.backoff.reset(), this.emitReserved("reconnect", e)
        }
      }
      const Ae = {};
  
      function we(e, t) {
        "object" == typeof e && (t = e, e = void 0);
        const r = function (e, t = "", r) {
            let i = e;
            r = r || "undefined" != typeof location && location, null == e && (e = r.protocol + "//" + r.host),
              "string" == typeof e && ("/" === e.charAt(0) && (e = "/" === e.charAt(1) ? r.protocol + e : r
                .host + e), /^(https?|wss?):\/\//.test(e) || (e = void 0 !== r ? r.protocol + "//" + e :
                "https://" + e), i = re(e)), i.port || (/^(http|ws)$/.test(i.protocol) ? i.port = "80" :
                /^(http|ws)s$/.test(i.protocol) && (i.port = "443")), i.path = i.path || "/";
            const n = -1 !== i.host.indexOf(":") ? "[" + i.host + "]" : i.host;
            return i.id = i.protocol + "://" + n + ":" + i.port + t, i.href = i.protocol + "://" + n + (r && r
              .port === i.port ? "" : ":" + i.port), i
          }(e, (t = t || {}).path || "/socket.io"),
          i = r.source,
          n = r.id,
          o = r.path,
          a = Ae[n] && o in Ae[n].nsps;
        let s;
        return t.forceNew || t["force new connection"] || !1 === t.multiplex || a ? s = new Le(i, t) : (Ae[n] ||
          (Ae[n] = new Le(i, t)), s = Ae[n]), r.query && !t.query && (t.query = r.queryKey), s.socket(r.path,
          t)
      }
  
      function ke() {
        return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, (function (e) {
          var t = 16 * Math.random() | 0;
          return ("x" === e ? t : 3 & t | 8).toString(16)
        }))
      }
  
      function Ne(e) {
        var t = arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : 100,
          r = arguments.length > 2 ? arguments[2] : void 0;
        return e = "".concat(e), r = r && ~e.indexOf(".") ? e.split(".").pop() : "", e.length > t && (e = e
          .substring(0, t - r.length) + "..." + r), e
      }
  
      function Ie(e) {
        for (var t = atob(e.split(",")[1]), r = e.substring(5, e.indexOf(";base64")), i = new Uint8Array(t
            .length), n = 0, o = t.length; n < o; n++) i[n] = t.charCodeAt(n);
        return new Blob([i], {
          type: r
        })
      }
  
      function De(e, t) {
        return function (e, t) {
          return new File([e], t, {
            type: e.type
          })
        }(Ie(e), t)
      }
  
      function Ce(e) {
        var t = arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : {},
          r = function (e) {
            var t = arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : {},
              r = t.format || "image/jpeg",
              i = t.quality || .8,
              n = t.scale || 1,
              o = e.videoWidth * n,
              a = e.videoHeight * n;
            if (o && a) {
              var s = document.createElement("canvas");
              return s.width = o, s.height = a, s.getContext("2d").drawImage(e, 0, 0, s.width, s.height), s
                .toDataURL(r, i)
            }
          }(e, t);
        return t.filename ? De(r, t.filename) : r
      }
  
      function ze() {
        var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {},
          t = Array.isArray(e) ? [] : {},
          r = [],
          i = function (i) {
            var n = e[i];
            (n = t[i] = "function" == typeof n ? n() : n) instanceof Promise ? r.push(n.then((e => t[i] = e))) :
              null !== n && "object" == typeof n && r.push(ze(n).then((e => t[i] = e)))
          };
        for (var n in e) i(n);
        return Promise.all(r).then((() => t))
      }
  
      function xe(e) {
        if (e) {
          var t = {},
            r = new RegExp(
              "^\\s*([^:]+)://(?:([^:@,/?&]+)(?::([^:@,/?&]+))?@)?([^@/?&]+)(?:/([^:@,/?&]+)?)?(?:\\?([^:@,/?]+)?)?\\s*$",
              "gi").exec(e);
          return Array.isArray(r) && (t.scheme = r[1], t.username = r[2] ? decodeURIComponent(r[2]) : r[2], t
            .password = r[3] ? decodeURIComponent(r[3]) : r[3], t.hosts = r[4].split(",").map((e => {
              var t = e.indexOf(":");
              return t >= 0 ? {
                host: decodeURIComponent(e.substring(0, t)),
                port: +e.substring(t + 1)
              } : {
                host: decodeURIComponent(e)
              }
            })), t.endpoint = r[5] ? decodeURIComponent(r[5]) : r[5], t.options = r[6] ? function (e) {
              var t = {};
              return e.split("&").forEach((e => {
                var r = e.indexOf("=");
                r >= 0 && (t[decodeURIComponent(e.substring(0, r))] = decodeURIComponent(e.substring(r +
                  1)))
              })), t
            }(r[6]) : r[6]), t
        }
      }
  
      function Ee(e) {
        var t = arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : {};
        return new Promise((function (r, i) {
          var n = t.body,
            o = t.method || (n ? "POST" : "GET"),
            a = !0 === t.credentials,
            s = t.timeout || 60,
            c = Object.assign({
              Authorization: "Bearer ".concat(Ee.token)
            }, t.headers || {}),
            l = t.progress;
          if (n instanceof File) {
            var d = new FormData;
            d.append("upload", n), n = d
          } else "object" == typeof n && (c["Content-Type"] = "application/json; charset=utf-8", n = JSON
            .stringify(n));
          var u = new XMLHttpRequest;
          for (var p in u.open(o, "".concat(Ee.url).concat(e), !0), c) u.setRequestHeader(p, c[p]);
          u.timeout = 1e3 * s, u.withCredentials = a, "function" == typeof l && u.upload.addEventListener(
            "progress", l, !1), u.onreadystatechange = function () {
            if (this.readyState === this.DONE) {
              var e;
              try {
                e = JSON.parse(this.responseText)
              } catch (e) {}
              if (200 === this.status) r(e || this.responseText);
              else {
                var t = (e = e || {}).message || this.statusText || "Request error",
                  n = new Error(t);
                e.name && (n.name = e.name), e.code && (n.code = e.code), i(n)
              }
            }
          }, u.send(n)
        }))
      }
      var Se;
      Object.assign(we, {
        Manager: Le,
        Socket: Pe,
        io: we,
        connect: we
      }), Ee.url = "".concat(location.origin).concat(location.pathname).replace(/\/$/, ""), Ee.token = "";
      var Oe = {
        get: e => e && Se ? e.split(".").reduce((function (e, t) {
          return e ? e[t] : e
        }), Se) : Se,
        filter(e) {
          if (Array.isArray(e) || (e = arguments), !e.length) return Oe.get();
          for (var t = {}, r = 0, i = e.length; r < i; r++) {
            var n = e[r],
              o = Oe.get(n);
            void 0 !== o && (t[n] = o)
          }
          return t
        },
        isAuth: () => !!Se,
        isMe: e => Se && Se.id === e,
        hasRole(e) {
          if (!Se) return !1;
          for (var t = [].concat(e), r = 0, i = t.length; r < i; r++)
            if (t[r] === Se.role) return !0;
          return !1
        },
        sync: e => Se = e,
        update: e => Ee("/api/user/update", {
          method: "POST",
          body: e
        }).then((e => e.id ? Se = e : Se))
      };
      const Re = Oe;
      var Qe, Ye, Ue = {},
        Ge = we("http://localhost", {
          autoConnect: !1,
          transports: ["websocket"]
        });
      Ge.on("connect", (function () {
        for (var e in Ue) Ge.emit("join", e);
        "function" == typeof Qe && (Qe(), Qe = null)
      })), Ge.io.on("error", (function (e) {
        "function" == typeof Ye && (Ye(e), Ye = null)
      }));
      var Be = {
        get id() {
          return Ge.id
        },
        get connected() {
          return Ge.connected
        },
        get user() {
          return btoa("".concat(Re.get("username"), "@").concat(Re.get("host")))
        },
        get group() {
          return btoa("".concat(Re.get("group"), "@").concat(Re.get("host")))
        },
        sync: () => new Promise(((e, t) => {
          if (Qe = e, Ye = t, Re.get("username")) {
            var r = Be.user;
            Ue[r] = !0
          }
          if (Re.get("group")) {
            var i = Be.group;
            Ue[i] = !0
          }
          Ge.io.opts.query = "token=".concat(Ee.token), Ge.io.uri = Ee.url, Ge.connected ? e() : Ge
            .open()
        })),
        close: () => (Ue = {}, Ge.close()),
        join(e, t) {
          if (e) return Ue[e] = !0, Ge.emit("join", e, t)
        },
        leave(e) {
          if (arguments.length) Ge && Ge.emit("leave", e), delete Ue[e];
          else
            for (var t in Ue) Ge && Ge.emit("leave", t), delete Ue[t]
        },
        on() {
          return Ge.on.apply(Ge, arguments)
        },
        off() {
          return Ge.off.apply(Ge, arguments)
        },
        emit() {
          return Ge.emit.apply(Ge, arguments)
        }
      };
      const Ke = Be;
      let He = !0,
        qe = !0;
  
      function We(e, t, r) {
        const i = e.match(t);
        return i && i.length >= r && parseInt(i[r], 10)
      }
  
      function Ve(e, t, r) {
        if (!e.RTCPeerConnection) return;
        const i = e.RTCPeerConnection.prototype,
          n = i.addEventListener;
        i.addEventListener = function (e, i) {
          if (e !== t) return n.apply(this, arguments);
          const o = e => {
            const t = r(e);
            t && (i.handleEvent ? i.handleEvent(t) : i(t))
          };
          return this._eventMap = this._eventMap || {}, this._eventMap[t] || (this._eventMap[t] = new Map),
            this._eventMap[t].set(i, o), n.apply(this, [e, o])
        };
        const o = i.removeEventListener;
        i.removeEventListener = function (e, r) {
          if (e !== t || !this._eventMap || !this._eventMap[t]) return o.apply(this, arguments);
          if (!this._eventMap[t].has(r)) return o.apply(this, arguments);
          const i = this._eventMap[t].get(r);
          return this._eventMap[t].delete(r), 0 === this._eventMap[t].size && delete this._eventMap[t], 0 ===
            Object.keys(this._eventMap).length && delete this._eventMap, o.apply(this, [e, i])
        }, Object.defineProperty(i, "on" + t, {
          get() {
            return this["_on" + t]
          },
          set(e) {
            this["_on" + t] && (this.removeEventListener(t, this["_on" + t]), delete this["_on" + t]),
              e && this.addEventListener(t, this["_on" + t] = e)
          },
          enumerable: !0,
          configurable: !0
        })
      }
  
      function Ze(e) {
        return "boolean" != typeof e ? new Error("Argument type: " + typeof e + ". Please use a boolean.") : (
          He = e, e ? "adapter.js logging disabled" : "adapter.js logging enabled")
      }
  
      function Fe(e) {
        return "boolean" != typeof e ? new Error("Argument type: " + typeof e + ". Please use a boolean.") : (
          qe = !e, "adapter.js deprecation warnings " + (e ? "disabled" : "enabled"))
      }
  
      function Je() {
        if ("object" == typeof window) {
          if (He) return;
          "undefined" != typeof console && "function" == typeof console.log && console.log.apply(console,
            arguments)
        }
      }
  
      function Xe(e, t) {
        qe && console.warn(e + " is deprecated, please use " + t + " instead.")
      }
  
      function _e(e) {
        return "[object Object]" === Object.prototype.toString.call(e)
      }
  
      function $e(e) {
        return _e(e) ? Object.keys(e).reduce((function (t, r) {
          const i = _e(e[r]),
            n = i ? $e(e[r]) : e[r],
            o = i && !Object.keys(n).length;
          return void 0 === n || o ? t : Object.assign(t, {
            [r]: n
          })
        }), {}) : e
      }
  
      function et(e, t, r) {
        t && !r.has(t.id) && (r.set(t.id, t), Object.keys(t).forEach((i => {
          i.endsWith("Id") ? et(e, e.get(t[i]), r) : i.endsWith("Ids") && t[i].forEach((t => {
            et(e, e.get(t), r)
          }))
        })))
      }
  
      function tt(e, t, r) {
        const i = r ? "outbound-rtp" : "inbound-rtp",
          n = new Map;
        if (null === t) return n;
        const o = [];
        return e.forEach((e => {
          "track" === e.type && e.trackIdentifier === t.id && o.push(e)
        })), o.forEach((t => {
          e.forEach((r => {
            r.type === i && r.trackId === t.id && et(e, r, n)
          }))
        })), n
      }
      const rt = Je;
  
      function it(e, t) {
        const r = e && e.navigator;
        if (!r.mediaDevices) return;
        const i = function (e) {
            if ("object" != typeof e || e.mandatory || e.optional) return e;
            const t = {};
            return Object.keys(e).forEach((r => {
              if ("require" === r || "advanced" === r || "mediaSource" === r) return;
              const i = "object" == typeof e[r] ? e[r] : {
                ideal: e[r]
              };
              void 0 !== i.exact && "number" == typeof i.exact && (i.min = i.max = i.exact);
              const n = function (e, t) {
                return e ? e + t.charAt(0).toUpperCase() + t.slice(1) : "deviceId" === t ? "sourceId" :
                  t
              };
              if (void 0 !== i.ideal) {
                t.optional = t.optional || [];
                let e = {};
                "number" == typeof i.ideal ? (e[n("min", r)] = i.ideal, t.optional.push(e), e = {}, e[n(
                  "max", r)] = i.ideal, t.optional.push(e)) : (e[n("", r)] = i.ideal, t.optional.push(
                  e))
              }
              void 0 !== i.exact && "number" != typeof i.exact ? (t.mandatory = t.mandatory || {}, t
                .mandatory[n("", r)] = i.exact) : ["min", "max"].forEach((e => {
                void 0 !== i[e] && (t.mandatory = t.mandatory || {}, t.mandatory[n(e, r)] = i[e])
              }))
            })), e.advanced && (t.optional = (t.optional || []).concat(e.advanced)), t
          },
          n = function (e, n) {
            if (t.version >= 61) return n(e);
            if ((e = JSON.parse(JSON.stringify(e))) && "object" == typeof e.audio) {
              const t = function (e, t, r) {
                t in e && !(r in e) && (e[r] = e[t], delete e[t])
              };
              t((e = JSON.parse(JSON.stringify(e))).audio, "autoGainControl", "googAutoGainControl"), t(e.audio,
                "noiseSuppression", "googNoiseSuppression"), e.audio = i(e.audio)
            }
            if (e && "object" == typeof e.video) {
              let o = e.video.facingMode;
              o = o && ("object" == typeof o ? o : {
                ideal: o
              });
              const a = t.version < 66;
              if (o && ("user" === o.exact || "environment" === o.exact || "user" === o.ideal ||
                  "environment" === o.ideal) && (!r.mediaDevices.getSupportedConstraints || !r.mediaDevices
                  .getSupportedConstraints().facingMode || a)) {
                let t;
                if (delete e.video.facingMode, "environment" === o.exact || "environment" === o.ideal ? t = [
                    "back", "rear"
                  ] : "user" !== o.exact && "user" !== o.ideal || (t = ["front"]), t) return r.mediaDevices
                  .enumerateDevices().then((r => {
                    let a = (r = r.filter((e => "videoinput" === e.kind))).find((e => t.some((t => e.label
                      .toLowerCase().includes(t)))));
                    return !a && r.length && t.includes("back") && (a = r[r.length - 1]), a && (e.video
                      .deviceId = o.exact ? {
                        exact: a.deviceId
                      } : {
                        ideal: a.deviceId
                      }), e.video = i(e.video), rt("chrome: " + JSON.stringify(e)), n(e)
                  }))
              }
              e.video = i(e.video)
            }
            return rt("chrome: " + JSON.stringify(e)), n(e)
          },
          o = function (e) {
            return t.version >= 64 ? e : {
              name: {
                PermissionDeniedError: "NotAllowedError",
                PermissionDismissedError: "NotAllowedError",
                InvalidStateError: "NotAllowedError",
                DevicesNotFoundError: "NotFoundError",
                ConstraintNotSatisfiedError: "OverconstrainedError",
                TrackStartError: "NotReadableError",
                MediaDeviceFailedDueToShutdown: "NotAllowedError",
                MediaDeviceKillSwitchOn: "NotAllowedError",
                TabCaptureError: "AbortError",
                ScreenCaptureError: "AbortError",
                DeviceCaptureError: "AbortError"
              } [e.name] || e.name,
              message: e.message,
              constraint: e.constraint || e.constraintName,
              toString() {
                return this.name + (this.message && ": ") + this.message
              }
            }
          };
        if (r.getUserMedia = function (e, t, i) {
            n(e, (e => {
              r.webkitGetUserMedia(e, t, (e => {
                i && i(o(e))
              }))
            }))
          }.bind(r), r.mediaDevices.getUserMedia) {
          const e = r.mediaDevices.getUserMedia.bind(r.mediaDevices);
          r.mediaDevices.getUserMedia = function (t) {
            return n(t, (t => e(t).then((e => {
              if (t.audio && !e.getAudioTracks().length || t.video && !e.getVideoTracks().length)
                throw e.getTracks().forEach((e => {
                  e.stop()
                })), new DOMException("", "NotFoundError");
              return e
            }), (e => Promise.reject(o(e))))))
          }
        }
      }
  
      function nt(e, t) {
        e.navigator.mediaDevices && "getDisplayMedia" in e.navigator.mediaDevices || e.navigator.mediaDevices &&
          ("function" == typeof t ? e.navigator.mediaDevices.getDisplayMedia = function (r) {
            return t(r).then((t => {
              const i = r.video && r.video.width,
                n = r.video && r.video.height,
                o = r.video && r.video.frameRate;
              return r.video = {
                  mandatory: {
                    chromeMediaSource: "desktop",
                    chromeMediaSourceId: t,
                    maxFrameRate: o || 3
                  }
                }, i && (r.video.mandatory.maxWidth = i), n && (r.video.mandatory.maxHeight = n), e
                .navigator.mediaDevices.getUserMedia(r)
            }))
          } : console.error("shimGetDisplayMedia: getSourceId argument is not a function"))
      }
  
      function ot(e) {
        e.MediaStream = e.MediaStream || e.webkitMediaStream
      }
  
      function at(e) {
        if ("object" == typeof e && e.RTCPeerConnection && !("ontrack" in e.RTCPeerConnection.prototype)) {
          Object.defineProperty(e.RTCPeerConnection.prototype, "ontrack", {
            get() {
              return this._ontrack
            },
            set(e) {
              this._ontrack && this.removeEventListener("track", this._ontrack), this.addEventListener(
                "track", this._ontrack = e)
            },
            enumerable: !0,
            configurable: !0
          });
          const t = e.RTCPeerConnection.prototype.setRemoteDescription;
          e.RTCPeerConnection.prototype.setRemoteDescription = function () {
            return this._ontrackpoly || (this._ontrackpoly = t => {
              t.stream.addEventListener("addtrack", (r => {
                let i;
                i = e.RTCPeerConnection.prototype.getReceivers ? this.getReceivers().find((e => e
                  .track && e.track.id === r.track.id)) : {
                  track: r.track
                };
                const n = new Event("track");
                n.track = r.track, n.receiver = i, n.transceiver = {
                  receiver: i
                }, n.streams = [t.stream], this.dispatchEvent(n)
              })), t.stream.getTracks().forEach((r => {
                let i;
                i = e.RTCPeerConnection.prototype.getReceivers ? this.getReceivers().find((e => e
                  .track && e.track.id === r.id)) : {
                  track: r
                };
                const n = new Event("track");
                n.track = r, n.receiver = i, n.transceiver = {
                  receiver: i
                }, n.streams = [t.stream], this.dispatchEvent(n)
              }))
            }, this.addEventListener("addstream", this._ontrackpoly)), t.apply(this, arguments)
          }
        } else Ve(e, "track", (e => (e.transceiver || Object.defineProperty(e, "transceiver", {
          value: {
            receiver: e.receiver
          }
        }), e)))
      }
  
      function st(e) {
        if ("object" == typeof e && e.RTCPeerConnection && !("getSenders" in e.RTCPeerConnection.prototype) &&
          "createDTMFSender" in e.RTCPeerConnection.prototype) {
          const t = function (e, t) {
            return {
              track: t,
              get dtmf() {
                return void 0 === this._dtmf && ("audio" === t.kind ? this._dtmf = e.createDTMFSender(t) :
                  this._dtmf = null), this._dtmf
              },
              _pc: e
            }
          };
          if (!e.RTCPeerConnection.prototype.getSenders) {
            e.RTCPeerConnection.prototype.getSenders = function () {
              return this._senders = this._senders || [], this._senders.slice()
            };
            const r = e.RTCPeerConnection.prototype.addTrack;
            e.RTCPeerConnection.prototype.addTrack = function (e, i) {
              let n = r.apply(this, arguments);
              return n || (n = t(this, e), this._senders.push(n)), n
            };
            const i = e.RTCPeerConnection.prototype.removeTrack;
            e.RTCPeerConnection.prototype.removeTrack = function (e) {
              i.apply(this, arguments);
              const t = this._senders.indexOf(e); - 1 !== t && this._senders.splice(t, 1)
            }
          }
          const r = e.RTCPeerConnection.prototype.addStream;
          e.RTCPeerConnection.prototype.addStream = function (e) {
            this._senders = this._senders || [], r.apply(this, [e]), e.getTracks().forEach((e => {
              this._senders.push(t(this, e))
            }))
          };
          const i = e.RTCPeerConnection.prototype.removeStream;
          e.RTCPeerConnection.prototype.removeStream = function (e) {
            this._senders = this._senders || [], i.apply(this, [e]), e.getTracks().forEach((e => {
              const t = this._senders.find((t => t.track === e));
              t && this._senders.splice(this._senders.indexOf(t), 1)
            }))
          }
        } else if ("object" == typeof e && e.RTCPeerConnection && "getSenders" in e.RTCPeerConnection
          .prototype && "createDTMFSender" in e.RTCPeerConnection.prototype && e.RTCRtpSender && !("dtmf" in e
            .RTCRtpSender.prototype)) {
          const t = e.RTCPeerConnection.prototype.getSenders;
          e.RTCPeerConnection.prototype.getSenders = function () {
            const e = t.apply(this, []);
            return e.forEach((e => e._pc = this)), e
          }, Object.defineProperty(e.RTCRtpSender.prototype, "dtmf", {
            get() {
              return void 0 === this._dtmf && ("audio" === this.track.kind ? this._dtmf = this._pc
                .createDTMFSender(this.track) : this._dtmf = null), this._dtmf
            }
          })
        }
      }
  
      function ct(e) {
        if (!e.RTCPeerConnection) return;
        const t = e.RTCPeerConnection.prototype.getStats;
        e.RTCPeerConnection.prototype.getStats = function () {
          const [e, r, i] = arguments;
          if (arguments.length > 0 && "function" == typeof e) return t.apply(this, arguments);
          if (0 === t.length && (0 === arguments.length || "function" != typeof e)) return t.apply(this, []);
          const n = function (e) {
              const t = {};
              return e.result().forEach((e => {
                const r = {
                  id: e.id,
                  timestamp: e.timestamp,
                  type: {
                    localcandidate: "local-candidate",
                    remotecandidate: "remote-candidate"
                  } [e.type] || e.type
                };
                e.names().forEach((t => {
                  r[t] = e.stat(t)
                })), t[r.id] = r
              })), t
            },
            o = function (e) {
              return new Map(Object.keys(e).map((t => [t, e[t]])))
            };
          if (arguments.length >= 2) {
            const i = function (e) {
              r(o(n(e)))
            };
            return t.apply(this, [i, e])
          }
          return new Promise(((e, r) => {
            t.apply(this, [function (t) {
              e(o(n(t)))
            }, r])
          })).then(r, i)
        }
      }
  
      function lt(e) {
        if (!("object" == typeof e && e.RTCPeerConnection && e.RTCRtpSender && e.RTCRtpReceiver)) return;
        if (!("getStats" in e.RTCRtpSender.prototype)) {
          const t = e.RTCPeerConnection.prototype.getSenders;
          t && (e.RTCPeerConnection.prototype.getSenders = function () {
            const e = t.apply(this, []);
            return e.forEach((e => e._pc = this)), e
          });
          const r = e.RTCPeerConnection.prototype.addTrack;
          r && (e.RTCPeerConnection.prototype.addTrack = function () {
            const e = r.apply(this, arguments);
            return e._pc = this, e
          }), e.RTCRtpSender.prototype.getStats = function () {
            const e = this;
            return this._pc.getStats().then((t => tt(t, e.track, !0)))
          }
        }
        if (!("getStats" in e.RTCRtpReceiver.prototype)) {
          const t = e.RTCPeerConnection.prototype.getReceivers;
          t && (e.RTCPeerConnection.prototype.getReceivers = function () {
              const e = t.apply(this, []);
              return e.forEach((e => e._pc = this)), e
            }), Ve(e, "track", (e => (e.receiver._pc = e.srcElement, e))), e.RTCRtpReceiver.prototype.getStats =
            function () {
              const e = this;
              return this._pc.getStats().then((t => tt(t, e.track, !1)))
            }
        }
        if (!("getStats" in e.RTCRtpSender.prototype) || !("getStats" in e.RTCRtpReceiver.prototype)) return;
        const t = e.RTCPeerConnection.prototype.getStats;
        e.RTCPeerConnection.prototype.getStats = function () {
          if (arguments.length > 0 && arguments[0] instanceof e.MediaStreamTrack) {
            const e = arguments[0];
            let t, r, i;
            return this.getSenders().forEach((r => {
                r.track === e && (t ? i = !0 : t = r)
              })), this.getReceivers().forEach((t => (t.track === e && (r ? i = !0 : r = t), t.track === e))),
              i || t && r ? Promise.reject(new DOMException(
                "There are more than one sender or receiver for the track.", "InvalidAccessError")) : t ? t
              .getStats() : r ? r.getStats() : Promise.reject(new DOMException(
                "There is no sender or receiver for the track.", "InvalidAccessError"))
          }
          return t.apply(this, arguments)
        }
      }
  
      function dt(e) {
        e.RTCPeerConnection.prototype.getLocalStreams = function () {
          return this._shimmedLocalStreams = this._shimmedLocalStreams || {}, Object.keys(this
            ._shimmedLocalStreams).map((e => this._shimmedLocalStreams[e][0]))
        };
        const t = e.RTCPeerConnection.prototype.addTrack;
        e.RTCPeerConnection.prototype.addTrack = function (e, r) {
          if (!r) return t.apply(this, arguments);
          this._shimmedLocalStreams = this._shimmedLocalStreams || {};
          const i = t.apply(this, arguments);
          return this._shimmedLocalStreams[r.id] ? -1 === this._shimmedLocalStreams[r.id].indexOf(i) && this
            ._shimmedLocalStreams[r.id].push(i) : this._shimmedLocalStreams[r.id] = [r, i], i
        };
        const r = e.RTCPeerConnection.prototype.addStream;
        e.RTCPeerConnection.prototype.addStream = function (e) {
          this._shimmedLocalStreams = this._shimmedLocalStreams || {}, e.getTracks().forEach((e => {
            if (this.getSenders().find((t => t.track === e))) throw new DOMException(
              "Track already exists.", "InvalidAccessError")
          }));
          const t = this.getSenders();
          r.apply(this, arguments);
          const i = this.getSenders().filter((e => -1 === t.indexOf(e)));
          this._shimmedLocalStreams[e.id] = [e].concat(i)
        };
        const i = e.RTCPeerConnection.prototype.removeStream;
        e.RTCPeerConnection.prototype.removeStream = function (e) {
          return this._shimmedLocalStreams = this._shimmedLocalStreams || {}, delete this
            ._shimmedLocalStreams[e.id], i.apply(this, arguments)
        };
        const n = e.RTCPeerConnection.prototype.removeTrack;
        e.RTCPeerConnection.prototype.removeTrack = function (e) {
          return this._shimmedLocalStreams = this._shimmedLocalStreams || {}, e && Object.keys(this
            ._shimmedLocalStreams).forEach((t => {
            const r = this._shimmedLocalStreams[t].indexOf(e); - 1 !== r && this._shimmedLocalStreams[t]
              .splice(r, 1), 1 === this._shimmedLocalStreams[t].length && delete this
              ._shimmedLocalStreams[t]
          })), n.apply(this, arguments)
        }
      }
  
      function ut(e, t) {
        if (!e.RTCPeerConnection) return;
        if (e.RTCPeerConnection.prototype.addTrack && t.version >= 65) return dt(e);
        const r = e.RTCPeerConnection.prototype.getLocalStreams;
        e.RTCPeerConnection.prototype.getLocalStreams = function () {
          const e = r.apply(this);
          return this._reverseStreams = this._reverseStreams || {}, e.map((e => this._reverseStreams[e.id]))
        };
        const i = e.RTCPeerConnection.prototype.addStream;
        e.RTCPeerConnection.prototype.addStream = function (t) {
          if (this._streams = this._streams || {}, this._reverseStreams = this._reverseStreams || {}, t
            .getTracks().forEach((e => {
              if (this.getSenders().find((t => t.track === e))) throw new DOMException(
                "Track already exists.", "InvalidAccessError")
            })), !this._reverseStreams[t.id]) {
            const r = new e.MediaStream(t.getTracks());
            this._streams[t.id] = r, this._reverseStreams[r.id] = t, t = r
          }
          i.apply(this, [t])
        };
        const n = e.RTCPeerConnection.prototype.removeStream;
  
        function o(e, t) {
          let r = t.sdp;
          return Object.keys(e._reverseStreams || []).forEach((t => {
            const i = e._reverseStreams[t],
              n = e._streams[i.id];
            r = r.replace(new RegExp(n.id, "g"), i.id)
          })), new RTCSessionDescription({
            type: t.type,
            sdp: r
          })
        }
        e.RTCPeerConnection.prototype.removeStream = function (e) {
          this._streams = this._streams || {}, this._reverseStreams = this._reverseStreams || {}, n.apply(
            this, [this._streams[e.id] || e]), delete this._reverseStreams[this._streams[e.id] ? this
            ._streams[e.id].id : e.id], delete this._streams[e.id]
        }, e.RTCPeerConnection.prototype.addTrack = function (t, r) {
          if ("closed" === this.signalingState) throw new DOMException(
            "The RTCPeerConnection's signalingState is 'closed'.", "InvalidStateError");
          const i = [].slice.call(arguments, 1);
          if (1 !== i.length || !i[0].getTracks().find((e => e === t))) throw new DOMException(
            "The adapter.js addTrack polyfill only supports a single  stream which is associated with the specified track.",
            "NotSupportedError");
          if (this.getSenders().find((e => e.track === t))) throw new DOMException("Track already exists.",
            "InvalidAccessError");
          this._streams = this._streams || {}, this._reverseStreams = this._reverseStreams || {};
          const n = this._streams[r.id];
          if (n) n.addTrack(t), Promise.resolve().then((() => {
            this.dispatchEvent(new Event("negotiationneeded"))
          }));
          else {
            const i = new e.MediaStream([t]);
            this._streams[r.id] = i, this._reverseStreams[i.id] = r, this.addStream(i)
          }
          return this.getSenders().find((e => e.track === t))
        }, ["createOffer", "createAnswer"].forEach((function (t) {
          const r = e.RTCPeerConnection.prototype[t],
            i = {
              [t]() {
                const e = arguments;
                return arguments.length && "function" == typeof arguments[0] ? r.apply(this, [t => {
                  const r = o(this, t);
                  e[0].apply(null, [r])
                }, t => {
                  e[1] && e[1].apply(null, t)
                }, arguments[2]]) : r.apply(this, arguments).then((e => o(this, e)))
              }
            };
          e.RTCPeerConnection.prototype[t] = i[t]
        }));
        const a = e.RTCPeerConnection.prototype.setLocalDescription;
        e.RTCPeerConnection.prototype.setLocalDescription = function () {
          return arguments.length && arguments[0].type ? (arguments[0] = function (e, t) {
            let r = t.sdp;
            return Object.keys(e._reverseStreams || []).forEach((t => {
              const i = e._reverseStreams[t],
                n = e._streams[i.id];
              r = r.replace(new RegExp(i.id, "g"), n.id)
            })), new RTCSessionDescription({
              type: t.type,
              sdp: r
            })
          }(this, arguments[0]), a.apply(this, arguments)) : a.apply(this, arguments)
        };
        const s = Object.getOwnPropertyDescriptor(e.RTCPeerConnection.prototype, "localDescription");
        Object.defineProperty(e.RTCPeerConnection.prototype, "localDescription", {
          get() {
            const e = s.get.apply(this);
            return "" === e.type ? e : o(this, e)
          }
        }), e.RTCPeerConnection.prototype.removeTrack = function (e) {
          if ("closed" === this.signalingState) throw new DOMException(
            "The RTCPeerConnection's signalingState is 'closed'.", "InvalidStateError");
          if (!e._pc) throw new DOMException(
            "Argument 1 of RTCPeerConnection.removeTrack does not implement interface RTCRtpSender.",
            "TypeError");
          if (!(e._pc === this)) throw new DOMException("Sender was not created by this connection.",
            "InvalidAccessError");
          let t;
          this._streams = this._streams || {}, Object.keys(this._streams).forEach((r => {
            this._streams[r].getTracks().find((t => e.track === t)) && (t = this._streams[r])
          })), t && (1 === t.getTracks().length ? this.removeStream(this._reverseStreams[t.id]) : t
            .removeTrack(e.track), this.dispatchEvent(new Event("negotiationneeded")))
        }
      }
  
      function pt(e, t) {
        !e.RTCPeerConnection && e.webkitRTCPeerConnection && (e.RTCPeerConnection = e.webkitRTCPeerConnection),
          e.RTCPeerConnection && t.version < 53 && ["setLocalDescription", "setRemoteDescription",
            "addIceCandidate"
          ].forEach((function (t) {
            const r = e.RTCPeerConnection.prototype[t],
              i = {
                [t]() {
                  return arguments[0] = new("addIceCandidate" === t ? e.RTCIceCandidate : e
                    .RTCSessionDescription)(arguments[0]), r.apply(this, arguments)
                }
              };
            e.RTCPeerConnection.prototype[t] = i[t]
          }))
      }
  
      function vt(e, t) {
        Ve(e, "negotiationneeded", (e => {
          const r = e.target;
          if (!(t.version < 72 || r.getConfiguration && "plan-b" === r.getConfiguration().sdpSemantics) ||
            "stable" === r.signalingState) return e
        }))
      }
  
      function mt(e, t) {
        const r = e && e.navigator,
          i = e && e.MediaStreamTrack;
        if (r.getUserMedia = function (e, t, i) {
            Xe("navigator.getUserMedia", "navigator.mediaDevices.getUserMedia"), r.mediaDevices.getUserMedia(e)
              .then(t, i)
          }, !(t.version > 55 && "autoGainControl" in r.mediaDevices.getSupportedConstraints())) {
          const e = function (e, t, r) {
              t in e && !(r in e) && (e[r] = e[t], delete e[t])
            },
            t = r.mediaDevices.getUserMedia.bind(r.mediaDevices);
          if (r.mediaDevices.getUserMedia = function (r) {
              return "object" == typeof r && "object" == typeof r.audio && (r = JSON.parse(JSON.stringify(r)),
                e(r.audio, "autoGainControl", "mozAutoGainControl"), e(r.audio, "noiseSuppression",
                  "mozNoiseSuppression")), t(r)
            }, i && i.prototype.getSettings) {
            const t = i.prototype.getSettings;
            i.prototype.getSettings = function () {
              const r = t.apply(this, arguments);
              return e(r, "mozAutoGainControl", "autoGainControl"), e(r, "mozNoiseSuppression",
                "noiseSuppression"), r
            }
          }
          if (i && i.prototype.applyConstraints) {
            const t = i.prototype.applyConstraints;
            i.prototype.applyConstraints = function (r) {
              return "audio" === this.kind && "object" == typeof r && (r = JSON.parse(JSON.stringify(r)), e(r,
                  "autoGainControl", "mozAutoGainControl"), e(r, "noiseSuppression", "mozNoiseSuppression")),
                t.apply(this, [r])
            }
          }
        }
      }
  
      function ht(e, t) {
        e.navigator.mediaDevices && "getDisplayMedia" in e.navigator.mediaDevices || e.navigator.mediaDevices &&
          (e.navigator.mediaDevices.getDisplayMedia = function (r) {
            if (!r || !r.video) {
              const e = new DOMException("getDisplayMedia without video constraints is undefined");
              return e.name = "NotFoundError", e.code = 8, Promise.reject(e)
            }
            return !0 === r.video ? r.video = {
              mediaSource: t
            } : r.video.mediaSource = t, e.navigator.mediaDevices.getUserMedia(r)
          })
      }
  
      function gt(e) {
        "object" == typeof e && e.RTCTrackEvent && "receiver" in e.RTCTrackEvent.prototype && !("transceiver" in
          e.RTCTrackEvent.prototype) && Object.defineProperty(e.RTCTrackEvent.prototype, "transceiver", {
          get() {
            return {
              receiver: this.receiver
            }
          }
        })
      }
  
      function bt(e, t) {
        if ("object" != typeof e || !e.RTCPeerConnection && !e.mozRTCPeerConnection) return;
        !e.RTCPeerConnection && e.mozRTCPeerConnection && (e.RTCPeerConnection = e.mozRTCPeerConnection), t
          .version < 53 && ["setLocalDescription", "setRemoteDescription", "addIceCandidate"].forEach((
            function (t) {
              const r = e.RTCPeerConnection.prototype[t],
                i = {
                  [t]() {
                    return arguments[0] = new("addIceCandidate" === t ? e.RTCIceCandidate : e
                      .RTCSessionDescription)(arguments[0]), r.apply(this, arguments)
                  }
                };
              e.RTCPeerConnection.prototype[t] = i[t]
            }));
        const r = {
            inboundrtp: "inbound-rtp",
            outboundrtp: "outbound-rtp",
            candidatepair: "candidate-pair",
            localcandidate: "local-candidate",
            remotecandidate: "remote-candidate"
          },
          i = e.RTCPeerConnection.prototype.getStats;
        e.RTCPeerConnection.prototype.getStats = function () {
          const [e, n, o] = arguments;
          return i.apply(this, [e || null]).then((e => {
            if (t.version < 53 && !n) try {
              e.forEach((e => {
                e.type = r[e.type] || e.type
              }))
            } catch (t) {
              if ("TypeError" !== t.name) throw t;
              e.forEach(((t, i) => {
                e.set(i, Object.assign({}, t, {
                  type: r[t.type] || t.type
                }))
              }))
            }
            return e
          })).then(n, o)
        }
      }
  
      function ft(e) {
        if ("object" != typeof e || !e.RTCPeerConnection || !e.RTCRtpSender) return;
        if (e.RTCRtpSender && "getStats" in e.RTCRtpSender.prototype) return;
        const t = e.RTCPeerConnection.prototype.getSenders;
        t && (e.RTCPeerConnection.prototype.getSenders = function () {
          const e = t.apply(this, []);
          return e.forEach((e => e._pc = this)), e
        });
        const r = e.RTCPeerConnection.prototype.addTrack;
        r && (e.RTCPeerConnection.prototype.addTrack = function () {
          const e = r.apply(this, arguments);
          return e._pc = this, e
        }), e.RTCRtpSender.prototype.getStats = function () {
          return this.track ? this._pc.getStats(this.track) : Promise.resolve(new Map)
        }
      }
  
      function yt(e) {
        if ("object" != typeof e || !e.RTCPeerConnection || !e.RTCRtpSender) return;
        if (e.RTCRtpSender && "getStats" in e.RTCRtpReceiver.prototype) return;
        const t = e.RTCPeerConnection.prototype.getReceivers;
        t && (e.RTCPeerConnection.prototype.getReceivers = function () {
            const e = t.apply(this, []);
            return e.forEach((e => e._pc = this)), e
          }), Ve(e, "track", (e => (e.receiver._pc = e.srcElement, e))), e.RTCRtpReceiver.prototype.getStats =
          function () {
            return this._pc.getStats(this.track)
          }
      }
  
      function Mt(e) {
        e.RTCPeerConnection && !("removeStream" in e.RTCPeerConnection.prototype) && (e.RTCPeerConnection
          .prototype.removeStream = function (e) {
            Xe("removeStream", "removeTrack"), this.getSenders().forEach((t => {
              t.track && e.getTracks().includes(t.track) && this.removeTrack(t)
            }))
          })
      }
  
      function jt(e) {
        e.DataChannel && !e.RTCDataChannel && (e.RTCDataChannel = e.DataChannel)
      }
  
      function Pt(e) {
        if ("object" != typeof e || !e.RTCPeerConnection) return;
        const t = e.RTCPeerConnection.prototype.addTransceiver;
        t && (e.RTCPeerConnection.prototype.addTransceiver = function () {
          this.setParametersPromises = [];
          let e = arguments[1] && arguments[1].sendEncodings;
          void 0 === e && (e = []), e = [...e];
          const r = e.length > 0;
          r && e.forEach((e => {
            if ("rid" in e) {
              if (!/^[a-z0-9]{0,16}$/i.test(e.rid)) throw new TypeError("Invalid RID value provided.")
            }
            if ("scaleResolutionDownBy" in e && !(parseFloat(e.scaleResolutionDownBy) >= 1))
            throw new RangeError("scale_resolution_down_by must be >= 1.0");
            if ("maxFramerate" in e && !(parseFloat(e.maxFramerate) >= 0)) throw new RangeError(
              "max_framerate must be >= 0.0")
          }));
          const i = t.apply(this, arguments);
          if (r) {
            const {
              sender: t
            } = i, r = t.getParameters();
            (!("encodings" in r) || 1 === r.encodings.length && 0 === Object.keys(r.encodings[0]).length) &&
            (r.encodings = e, t.sendEncodings = e, this.setParametersPromises.push(t.setParameters(r).then((
              () => {
                delete t.sendEncodings
              })).catch((() => {
              delete t.sendEncodings
            }))))
          }
          return i
        })
      }
  
      function Tt(e) {
        if ("object" != typeof e || !e.RTCRtpSender) return;
        const t = e.RTCRtpSender.prototype.getParameters;
        t && (e.RTCRtpSender.prototype.getParameters = function () {
          const e = t.apply(this, arguments);
          return "encodings" in e || (e.encodings = [].concat(this.sendEncodings || [{}])), e
        })
      }
  
      function Lt(e) {
        if ("object" != typeof e || !e.RTCPeerConnection) return;
        const t = e.RTCPeerConnection.prototype.createOffer;
        e.RTCPeerConnection.prototype.createOffer = function () {
          return this.setParametersPromises && this.setParametersPromises.length ? Promise.all(this
            .setParametersPromises).then((() => t.apply(this, arguments))).finally((() => {
            this.setParametersPromises = []
          })) : t.apply(this, arguments)
        }
      }
  
      function At(e) {
        if ("object" != typeof e || !e.RTCPeerConnection) return;
        const t = e.RTCPeerConnection.prototype.createAnswer;
        e.RTCPeerConnection.prototype.createAnswer = function () {
          return this.setParametersPromises && this.setParametersPromises.length ? Promise.all(this
            .setParametersPromises).then((() => t.apply(this, arguments))).finally((() => {
            this.setParametersPromises = []
          })) : t.apply(this, arguments)
        }
      }
  
      function wt(e) {
        if ("object" == typeof e && e.RTCPeerConnection) {
          if ("getLocalStreams" in e.RTCPeerConnection.prototype || (e.RTCPeerConnection.prototype
              .getLocalStreams = function () {
                return this._localStreams || (this._localStreams = []), this._localStreams
              }), !("addStream" in e.RTCPeerConnection.prototype)) {
            const t = e.RTCPeerConnection.prototype.addTrack;
            e.RTCPeerConnection.prototype.addStream = function (e) {
              this._localStreams || (this._localStreams = []), this._localStreams.includes(e) || this
                ._localStreams.push(e), e.getAudioTracks().forEach((r => t.call(this, r, e))), e
                .getVideoTracks().forEach((r => t.call(this, r, e)))
            }, e.RTCPeerConnection.prototype.addTrack = function (e, ...r) {
              return r && r.forEach((e => {
                this._localStreams ? this._localStreams.includes(e) || this._localStreams.push(e) : this
                  ._localStreams = [e]
              })), t.apply(this, arguments)
            }
          }
          "removeStream" in e.RTCPeerConnection.prototype || (e.RTCPeerConnection.prototype.removeStream =
            function (e) {
              this._localStreams || (this._localStreams = []);
              const t = this._localStreams.indexOf(e);
              if (-1 === t) return;
              this._localStreams.splice(t, 1);
              const r = e.getTracks();
              this.getSenders().forEach((e => {
                r.includes(e.track) && this.removeTrack(e)
              }))
            })
        }
      }
  
      function kt(e) {
        if ("object" == typeof e && e.RTCPeerConnection && ("getRemoteStreams" in e.RTCPeerConnection
            .prototype || (e.RTCPeerConnection.prototype.getRemoteStreams = function () {
              return this._remoteStreams ? this._remoteStreams : []
            }), !("onaddstream" in e.RTCPeerConnection.prototype))) {
          Object.defineProperty(e.RTCPeerConnection.prototype, "onaddstream", {
            get() {
              return this._onaddstream
            },
            set(e) {
              this._onaddstream && (this.removeEventListener("addstream", this._onaddstream), this
                .removeEventListener("track", this._onaddstreampoly)), this.addEventListener(
                "addstream", this._onaddstream = e), this.addEventListener("track", this
                ._onaddstreampoly = e => {
                  e.streams.forEach((e => {
                    if (this._remoteStreams || (this._remoteStreams = []), this._remoteStreams
                      .includes(e)) return;
                    this._remoteStreams.push(e);
                    const t = new Event("addstream");
                    t.stream = e, this.dispatchEvent(t)
                  }))
                })
            }
          });
          const t = e.RTCPeerConnection.prototype.setRemoteDescription;
          e.RTCPeerConnection.prototype.setRemoteDescription = function () {
            const e = this;
            return this._onaddstreampoly || this.addEventListener("track", this._onaddstreampoly = function (
              t) {
              t.streams.forEach((t => {
                if (e._remoteStreams || (e._remoteStreams = []), e._remoteStreams.indexOf(t) >= 0)
                  return;
                e._remoteStreams.push(t);
                const r = new Event("addstream");
                r.stream = t, e.dispatchEvent(r)
              }))
            }), t.apply(e, arguments)
          }
        }
      }
  
      function Nt(e) {
        if ("object" != typeof e || !e.RTCPeerConnection) return;
        const t = e.RTCPeerConnection.prototype,
          r = t.createOffer,
          i = t.createAnswer,
          n = t.setLocalDescription,
          o = t.setRemoteDescription,
          a = t.addIceCandidate;
        t.createOffer = function (e, t) {
          const i = arguments.length >= 2 ? arguments[2] : arguments[0],
            n = r.apply(this, [i]);
          return t ? (n.then(e, t), Promise.resolve()) : n
        }, t.createAnswer = function (e, t) {
          const r = arguments.length >= 2 ? arguments[2] : arguments[0],
            n = i.apply(this, [r]);
          return t ? (n.then(e, t), Promise.resolve()) : n
        };
        let s = function (e, t, r) {
          const i = n.apply(this, [e]);
          return r ? (i.then(t, r), Promise.resolve()) : i
        };
        t.setLocalDescription = s, s = function (e, t, r) {
          const i = o.apply(this, [e]);
          return r ? (i.then(t, r), Promise.resolve()) : i
        }, t.setRemoteDescription = s, s = function (e, t, r) {
          const i = a.apply(this, [e]);
          return r ? (i.then(t, r), Promise.resolve()) : i
        }, t.addIceCandidate = s
      }
  
      function It(e) {
        const t = e && e.navigator;
        if (t.mediaDevices && t.mediaDevices.getUserMedia) {
          const e = t.mediaDevices,
            r = e.getUserMedia.bind(e);
          t.mediaDevices.getUserMedia = e => r(Dt(e))
        }!t.getUserMedia && t.mediaDevices && t.mediaDevices.getUserMedia && (t.getUserMedia = function (e, r,
          i) {
          t.mediaDevices.getUserMedia(e).then(r, i)
        }.bind(t))
      }
  
      function Dt(e) {
        return e && void 0 !== e.video ? Object.assign({}, e, {
          video: $e(e.video)
        }) : e
      }
  
      function Ct(e) {
        if (!e.RTCPeerConnection) return;
        const t = e.RTCPeerConnection;
        e.RTCPeerConnection = function (e, r) {
          if (e && e.iceServers) {
            const t = [];
            for (let r = 0; r < e.iceServers.length; r++) {
              let i = e.iceServers[r];
              void 0 === i.urls && i.url ? (Xe("RTCIceServer.url", "RTCIceServer.urls"), i = JSON.parse(JSON
                .stringify(i)), i.urls = i.url, delete i.url, t.push(i)) : t.push(e.iceServers[r])
            }
            e.iceServers = t
          }
          return new t(e, r)
        }, e.RTCPeerConnection.prototype = t.prototype, "generateCertificate" in t && Object.defineProperty(e
          .RTCPeerConnection, "generateCertificate", {
            get: () => t.generateCertificate
          })
      }
  
      function zt(e) {
        "object" == typeof e && e.RTCTrackEvent && "receiver" in e.RTCTrackEvent.prototype && !("transceiver" in
          e.RTCTrackEvent.prototype) && Object.defineProperty(e.RTCTrackEvent.prototype, "transceiver", {
          get() {
            return {
              receiver: this.receiver
            }
          }
        })
      }
  
      function xt(e) {
        const t = e.RTCPeerConnection.prototype.createOffer;
        e.RTCPeerConnection.prototype.createOffer = function (e) {
          if (e) {
            void 0 !== e.offerToReceiveAudio && (e.offerToReceiveAudio = !!e.offerToReceiveAudio);
            const t = this.getTransceivers().find((e => "audio" === e.receiver.track.kind));
            !1 === e.offerToReceiveAudio && t ? "sendrecv" === t.direction ? t.setDirection ? t.setDirection(
                "sendonly") : t.direction = "sendonly" : "recvonly" === t.direction && (t.setDirection ? t
                .setDirection("inactive") : t.direction = "inactive") : !0 !== e.offerToReceiveAudio || t ||
              this.addTransceiver("audio", {
                direction: "recvonly"
              }), void 0 !== e.offerToReceiveVideo && (e.offerToReceiveVideo = !!e.offerToReceiveVideo);
            const r = this.getTransceivers().find((e => "video" === e.receiver.track.kind));
            !1 === e.offerToReceiveVideo && r ? "sendrecv" === r.direction ? r.setDirection ? r.setDirection(
                "sendonly") : r.direction = "sendonly" : "recvonly" === r.direction && (r.setDirection ? r
                .setDirection("inactive") : r.direction = "inactive") : !0 !== e.offerToReceiveVideo || r ||
              this.addTransceiver("video", {
                direction: "recvonly"
              })
          }
          return t.apply(this, arguments)
        }
      }
  
      function Et(e) {
        "object" != typeof e || e.AudioContext || (e.AudioContext = e.webkitAudioContext)
      }
      var St = r(2281),
        Ot = r.n(St);
  
      function Rt(e) {
        if (!e.RTCIceCandidate || e.RTCIceCandidate && "foundation" in e.RTCIceCandidate.prototype) return;
        const t = e.RTCIceCandidate;
        e.RTCIceCandidate = function (e) {
          if ("object" == typeof e && e.candidate && 0 === e.candidate.indexOf("a=") && ((e = JSON.parse(JSON
              .stringify(e))).candidate = e.candidate.substring(2)), e.candidate && e.candidate.length) {
            const r = new t(e),
              i = Ot().parseCandidate(e.candidate);
            for (const e in i) e in r || Object.defineProperty(r, e, {
              value: i[e]
            });
            return r.toJSON = function () {
              return {
                candidate: r.candidate,
                sdpMid: r.sdpMid,
                sdpMLineIndex: r.sdpMLineIndex,
                usernameFragment: r.usernameFragment
              }
            }, r
          }
          return new t(e)
        }, e.RTCIceCandidate.prototype = t.prototype, Ve(e, "icecandidate", (t => (t.candidate && Object
          .defineProperty(t, "candidate", {
            value: new e.RTCIceCandidate(t.candidate),
            writable: "false"
          }), t)))
      }
  
      function Qt(e) {
        !e.RTCIceCandidate || e.RTCIceCandidate && "relayProtocol" in e.RTCIceCandidate.prototype || Ve(e,
          "icecandidate", (e => {
            if (e.candidate) {
              const t = Ot().parseCandidate(e.candidate.candidate);
              "relay" === t.type && (e.candidate.relayProtocol = {
                0: "tls",
                1: "tcp",
                2: "udp"
              } [t.priority >> 24])
            }
            return e
          }))
      }
  
      function Yt(e, t) {
        if (!e.RTCPeerConnection) return;
        "sctp" in e.RTCPeerConnection.prototype || Object.defineProperty(e.RTCPeerConnection.prototype,
        "sctp", {
          get() {
            return void 0 === this._sctp ? null : this._sctp
          }
        });
        const r = e.RTCPeerConnection.prototype.setRemoteDescription;
        e.RTCPeerConnection.prototype.setRemoteDescription = function () {
          if (this._sctp = null, "chrome" === t.browser && t.version >= 76) {
            const {
              sdpSemantics: e
            } = this.getConfiguration();
            "plan-b" === e && Object.defineProperty(this, "sctp", {
              get() {
                return void 0 === this._sctp ? null : this._sctp
              },
              enumerable: !0,
              configurable: !0
            })
          }
          if (function (e) {
              if (!e || !e.sdp) return !1;
              const t = Ot().splitSections(e.sdp);
              return t.shift(), t.some((e => {
                const t = Ot().parseMLine(e);
                return t && "application" === t.kind && -1 !== t.protocol.indexOf("SCTP")
              }))
            }(arguments[0])) {
            const e = function (e) {
                const t = e.sdp.match(/mozilla...THIS_IS_SDPARTA-(\d+)/);
                if (null === t || t.length < 2) return -1;
                const r = parseInt(t[1], 10);
                return r != r ? -1 : r
              }(arguments[0]),
              r = function (e) {
                let r = 65536;
                return "firefox" === t.browser && (r = t.version < 57 ? -1 === e ? 16384 : 2147483637 : t
                  .version < 60 ? 57 === t.version ? 65535 : 65536 : 2147483637), r
              }(e),
              i = function (e, r) {
                let i = 65536;
                "firefox" === t.browser && 57 === t.version && (i = 65535);
                const n = Ot().matchPrefix(e.sdp, "a=max-message-size:");
                return n.length > 0 ? i = parseInt(n[0].substring(19), 10) : "firefox" === t.browser && -1 !==
                  r && (i = 2147483637), i
              }(arguments[0], e);
            let n;
            n = 0 === r && 0 === i ? Number.POSITIVE_INFINITY : 0 === r || 0 === i ? Math.max(r, i) : Math
              .min(r, i);
            const o = {};
            Object.defineProperty(o, "maxMessageSize", {
              get: () => n
            }), this._sctp = o
          }
          return r.apply(this, arguments)
        }
      }
  
      function Ut(e) {
        if (!e.RTCPeerConnection || !("createDataChannel" in e.RTCPeerConnection.prototype)) return;
  
        function t(e, t) {
          const r = e.send;
          e.send = function () {
            const i = arguments[0],
              n = i.length || i.size || i.byteLength;
            if ("open" === e.readyState && t.sctp && n > t.sctp.maxMessageSize) throw new TypeError(
              "Message too large (can send a maximum of " + t.sctp.maxMessageSize + " bytes)");
            return r.apply(e, arguments)
          }
        }
        const r = e.RTCPeerConnection.prototype.createDataChannel;
        e.RTCPeerConnection.prototype.createDataChannel = function () {
          const e = r.apply(this, arguments);
          return t(e, this), e
        }, Ve(e, "datachannel", (e => (t(e.channel, e.target), e)))
      }
  
      function Gt(e) {
        if (!e.RTCPeerConnection || "connectionState" in e.RTCPeerConnection.prototype) return;
        const t = e.RTCPeerConnection.prototype;
        Object.defineProperty(t, "connectionState", {
          get() {
            return {
              completed: "connected",
              checking: "connecting"
            } [this.iceConnectionState] || this.iceConnectionState
          },
          enumerable: !0,
          configurable: !0
        }), Object.defineProperty(t, "onconnectionstatechange", {
          get() {
            return this._onconnectionstatechange || null
          },
          set(e) {
            this._onconnectionstatechange && (this.removeEventListener("connectionstatechange", this
                ._onconnectionstatechange), delete this._onconnectionstatechange), e && this
              .addEventListener("connectionstatechange", this._onconnectionstatechange = e)
          },
          enumerable: !0,
          configurable: !0
        }), ["setLocalDescription", "setRemoteDescription"].forEach((e => {
          const r = t[e];
          t[e] = function () {
            return this._connectionstatechangepoly || (this._connectionstatechangepoly = e => {
                const t = e.target;
                if (t._lastConnectionState !== t.connectionState) {
                  t._lastConnectionState = t.connectionState;
                  const r = new Event("connectionstatechange", e);
                  t.dispatchEvent(r)
                }
                return e
              }, this.addEventListener("iceconnectionstatechange", this._connectionstatechangepoly)), r
              .apply(this, arguments)
          }
        }))
      }
  
      function Bt(e, t) {
        if (!e.RTCPeerConnection) return;
        if ("chrome" === t.browser && t.version >= 71) return;
        if ("safari" === t.browser && t.version >= 605) return;
        const r = e.RTCPeerConnection.prototype.setRemoteDescription;
        e.RTCPeerConnection.prototype.setRemoteDescription = function (t) {
          if (t && t.sdp && -1 !== t.sdp.indexOf("\na=extmap-allow-mixed")) {
            const r = t.sdp.split("\n").filter((e => "a=extmap-allow-mixed" !== e.trim())).join("\n");
            e.RTCSessionDescription && t instanceof e.RTCSessionDescription ? arguments[0] = new e
              .RTCSessionDescription({
                type: t.type,
                sdp: r
              }) : t.sdp = r
          }
          return r.apply(this, arguments)
        }
      }
  
      function Kt(e, t) {
        if (!e.RTCPeerConnection || !e.RTCPeerConnection.prototype) return;
        const r = e.RTCPeerConnection.prototype.addIceCandidate;
        r && 0 !== r.length && (e.RTCPeerConnection.prototype.addIceCandidate = function () {
          return arguments[0] ? ("chrome" === t.browser && t.version < 78 || "firefox" === t.browser && t
              .version < 68 || "safari" === t.browser) && arguments[0] && "" === arguments[0].candidate ?
            Promise.resolve() : r.apply(this, arguments) : (arguments[1] && arguments[1].apply(null),
              Promise.resolve())
        })
      }
  
      function Ht(e, t) {
        if (!e.RTCPeerConnection || !e.RTCPeerConnection.prototype) return;
        const r = e.RTCPeerConnection.prototype.setLocalDescription;
        r && 0 !== r.length && (e.RTCPeerConnection.prototype.setLocalDescription = function () {
          let e = arguments[0] || {};
          if ("object" != typeof e || e.type && e.sdp) return r.apply(this, arguments);
          if (e = {
              type: e.type,
              sdp: e.sdp
            }, !e.type) switch (this.signalingState) {
          case "stable":
          case "have-local-offer":
          case "have-remote-pranswer":
            e.type = "offer";
            break;
          default:
            e.type = "answer"
          }
          if (e.sdp || "offer" !== e.type && "answer" !== e.type) return r.apply(this, [e]);
          return ("offer" === e.type ? this.createOffer : this.createAnswer).apply(this).then((e => r.apply(
            this, [e])))
        })
      }
      const qt = function ({
          window: e
        } = {}, r = {
          shimChrome: !0,
          shimFirefox: !0,
          shimSafari: !0
        }) {
          const i = Je,
            a = function (e) {
              const t = {
                browser: null,
                version: null
              };
              if (void 0 === e || !e.navigator) return t.browser = "Not a browser.", t;
              const {
                navigator: r
              } = e;
              if (r.mozGetUserMedia) t.browser = "firefox", t.version = We(r.userAgent, /Firefox\/(\d+)\./, 1);
              else if (r.webkitGetUserMedia || !1 === e.isSecureContext && e.webkitRTCPeerConnection) t
                .browser = "chrome", t.version = We(r.userAgent, /Chrom(e|ium)\/(\d+)\./, 2);
              else {
                if (!e.RTCPeerConnection || !r.userAgent.match(/AppleWebKit\/(\d+)\./)) return t.browser =
                  "Not a supported browser.", t;
                t.browser = "safari", t.version = We(r.userAgent, /AppleWebKit\/(\d+)\./, 1), t
                  .supportsUnifiedPlan = e.RTCRtpTransceiver && "currentDirection" in e.RTCRtpTransceiver
                  .prototype
              }
              return t
            }(e),
            c = {
              browserDetails: a,
              commonShim: s,
              extractVersion: We,
              disableLog: Ze,
              disableWarnings: Fe,
              sdp: St
            };
          switch (a.browser) {
          case "chrome":
            if (!t || !pt || !r.shimChrome) return i("Chrome shim is not included in this adapter release."), c;
            if (null === a.version) return i("Chrome shim can not determine version, not shimming."), c;
            i("adapter.js shimming chrome."), c.browserShim = t, Kt(e, a), Ht(e), it(e, a), ot(e), pt(e, a), at(
              e), ut(e, a), st(e), ct(e), lt(e), vt(e, a), Rt(e), Qt(e), Gt(e), Yt(e, a), Ut(e), Bt(e, a);
            break;
          case "firefox":
            if (!n || !bt || !r.shimFirefox) return i("Firefox shim is not included in this adapter release."),
              c;
            i("adapter.js shimming firefox."), c.browserShim = n, Kt(e, a), Ht(e), mt(e, a), bt(e, a), gt(e),
              Mt(e), ft(e), yt(e), jt(e), Pt(e), Tt(e), Lt(e), At(e), Rt(e), Gt(e), Yt(e, a), Ut(e);
            break;
          case "safari":
            if (!o || !r.shimSafari) return i("Safari shim is not included in this adapter release."), c;
            i("adapter.js shimming safari."), c.browserShim = o, Kt(e, a), Ht(e), Ct(e), xt(e), Nt(e), wt(e),
              kt(e), zt(e), It(e), Et(e), Rt(e), Qt(e), Yt(e, a), Ut(e), Bt(e, a);
            break;
          default:
            i("Unsupported browser!")
          }
          return c
        }({
          window: "undefined" == typeof window ? void 0 : window
        }),
        Wt = qt;
  
      function Vt(e) {
        return new Promise(((t, r) => {
          if (e || (e = {}), "screen" === e.source) {
            if (Jt()) return void(t => {
              var r = {
                audio: !1,
                video: {
                  aspectRatio: window.screen.width / window.screen.height,
                  width: {
                    max: e.width || Math.min(1280, window.screen.width)
                  },
                  height: {
                    max: e.height || Math.min(720, window.screen.height)
                  },
                  frameRate: {
                    max: e.frameRate || 5
                  }
                }
              };
              navigator.mediaDevices.getDisplayMedia(r).then((i => {
                if (e.displaySurface && "monitor" !== e.displaySurface) return t(null, i, r);
                var n = i.getVideoTracks()[0],
                  o = n.getSettings().displaySurface,
                  a = Wt.browserDetails.browser;
                if ("chrome" === a && "monitor" !== o || "firefox" === a &&
                  "Primary Monitor" !== n.label) return i.getTracks().forEach((e => e
                .stop())), t(new Error('Display surface "'.concat(o || n.label,
                    '" not allowed')));
                t(null, i, r)
              })).catch((() => t(new Error("Screen source is not set"))))
            })(((e, i) => {
              if (!e) return t(i);
              r(e)
            }));
            var i = Wt.browserDetails.browser;
            return "chrome" === i || "firefox" === i ? void(t => {
              var r = {
                audio: !1,
                video: {
                  mandatory: {
                    chromeMediaSource: "screen",
                    maxWidth: e.width || Math.min(1280, window.screen.width),
                    maxHeight: e.height || Math.min(720, window.screen.height),
                    maxFrameRate: e.frameRate || 5
                  },
                  mozMediaSource: "screen",
                  mediaSource: "screen"
                }
              };
              navigator.mediaDevices.getUserMedia(r).then((e => t(null, e, r))).catch((e => t(e)))
            })(((e, i) => {
              if (!e) return t(i);
              r(e)
            })) : r(new Error("Browser does not support screen capture"))
          }
          var n = {
            audio: !1 !== e.audio && {
              deviceId: e.audioDeviceId ? {
                exact: e.audioDeviceId
              } : void 0,
              autoGainControl: !1
            },
            video: !1 !== e.video && {
              deviceId: e.videoDeviceId ? {
                exact: e.videoDeviceId
              } : void 0,
              width: {
                ideal: e.width || 640
              },
              height: {
                ideal: e.height || 480
              },
              frameRate: {
                ideal: e.frameRate || 10
              },
              facingMode: {
                ideal: e.facingMode || "user"
              }
            }
          };
          return !1 === e.audio || !1 === e.video ? navigator.mediaDevices.getUserMedia(n).then((e => t(
              e))).catch((e => r(e))) : void navigator.mediaDevices.getUserMedia(n).then((e => t(e)))
            .catch((() => {
              var e = {
                audio: !1,
                video: n.video
              };
              navigator.mediaDevices.getUserMedia(e).then((e => t(e))).catch((() => {
                var e = {
                  audio: n.audio,
                  video: !1
                };
                navigator.mediaDevices.getUserMedia(e).then((e => t(e))).catch((e => r(e)))
              }))
            }))
        }))
      }
  
      function Zt() {
        var e = /iPad|iPhone|iPod/.test(navigator.userAgent) || /MacIntel/.test(navigator.userAgent) &&
          navigator.maxTouchPoints > 1,
          t = /Android/.test(navigator.userAgent) || /Linux/.test(navigator.userAgent) && navigator
          .maxTouchPoints > 1;
        return e || t
      }
  
      function Ft() {
        return /SEB/.test(navigator.userAgent)
      }
  
      function Jt() {
        return "function" == typeof navigator.mediaDevices.getDisplayMedia && !(window.chrome && !window.chrome
          .app)
      }
  
      function Xt() {
        var e, t = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {},
          r = t.el,
          i = t.muted,
          n = t.loop,
          o = t.controls,
          a = t.spinner,
          s = t.mirror,
          c = t.local,
          l = r || document.createElement("video");
        (l.playsinline = !0, l.setAttribute("playsinline", ""), l.autoplay = !0, l.setAttribute("autoplay", ""),
          l.disablePictureInPicture = !0, l.setAttribute("disablepictureinpicture", ""), l.oncontextmenu =
          function () {
            return !1
          }, l.muted = !!i, l.loop = !!n, l.controls = !!o, l.controlslist =
          "nodownload nofullscreen noremoteplayback", a && (l.dataset.spinner = !0), s && (l.dataset.mirror = !
            0), c && (l.dataset.local = !0), void 0 === l.srcObject) && Object.defineProperty(l, "srcObject", {
          get: function () {
            return e
          },
          set: function (t) {
            t ? l.src = URL.createObjectURL(t) : l.src && (URL.revokeObjectURL(l.src), l.removeAttribute(
              "src")), e = t
          }
        });
        var d = e => {
          var t = "get" + e + "Tracks";
          return {
            get() {
              var e = l.srcObject;
              if (!e) return !1;
              for (var r = e[t](), i = 0; i < r.length; i++) {
                if (!r[i].enabled) return !1
              }
              return !0
            },
            set(e) {
              var r = l.srcObject;
              if (r)
                for (var i = r[t](), n = 0; n < i.length; n++) {
                  i[n].enabled = e
                }
            }
          }
        };
        Object.defineProperties(l, {
          audioEnabled: d("Audio"),
          videoEnabled: d("Video"),
          enabled: {
            get() {
              return this.audioEnabled || this.videoEnabled
            },
            set(e) {
              this.audioEnabled = e, this.videoEnabled = e
            }
          }
        }), l.stop = function () {
          var e, t;
          null !== (e = this.srcObject) && void 0 !== e && e.active && (null === (t = this.srcObject) ||
            void 0 === t || t.getTracks().forEach((e => e.stop())))
        };
        var u = {
          playing: () => {
            a && delete l.dataset.spinner
          },
          click: () => {
            var e = l.play();
            e && "undefined" != typeof Promise && e instanceof Promise && e.catch((function () {}))
          }
        };
        for (var p in u) l.addEventListener(p, u[p]);
        return l
      }
  
      function _t(e, t, r) {
        if (!r) return e;
        var i, n, o = function (e) {
          return Object.keys(e).map((t => "".concat(t, "=").concat(e[t]))).join(";")
        };
        if (n = new RegExp("a=rtpmap:([0-9]+) ".concat(t)), !(i = e.match(n))) return e;
        var a = i[1];
        if (n = new RegExp("a=fmtp:".concat(a, " ([^\r\n]+)")), i = e.match(n)) {
          var s = i[1];
          r = Object.assign(s.split(";").reduce(((e, t) => {
            var r = (t = t.trim().split("="))[0],
              i = t[1];
            return e[r] = i, e
          }), {}), r), n = new RegExp("(a=fmtp:".concat(a, ") [^\r\n]+")), e = e.replace(n, "$1 ".concat(o(
            r)))
        } else n = new RegExp("(a=rtpmap:".concat(a, " ").concat(t, ")")), e = e.replace(n, "$1\r\na=fmtp:"
          .concat(a, " ").concat(o(r)));
        return e
      }
  
      function $t(e, t, r) {
        var i, n;
        if (i = new RegExp("a=rtpmap:([0-9]+) ".concat(r)), !(n = e.match(i))) return e;
        var o = n[1];
        if (i = new RegExp("m=".concat(t, " [^\\s]+ [^\\s]+ ([0-9 ]+)")), !(n = e.match(i))) return e;
        var a = n[1].split(" ");
        if (a[0] !== o) {
          var s = a.indexOf(o); - 1 !== s && a.splice(s, 1), a.unshift(o), i = new RegExp("(m=".concat(t,
            " [^\\s]+ [^\\s]+) [0-9 ]+")), e = e.replace(i, "$1 ".concat(a.join(" ")))
        }
        return e
      }
      class er {
        constructor(e) {
          this._config = e || {}, this._handlers = {}, this._events = {}, this._peers = {}, this._streams = {}
        }
        static createOffer() {
          var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {};
          return new Promise(((t, r) => {
            var i, n = e.id,
              o = e.from,
              a = e.stream,
              s = e.room,
              c = e.user,
              l = e.data,
              d = e.config,
              u = e.bitrate,
              p = e.ondispose,
              v = d.turnURI,
              m = u || {},
              h = m.audio,
              g = void 0 === h ? 16 : h,
              b = m.video,
              f = void 0 === b ? 64 : b,
              y = new RTCPeerConnection({
                iceServers: er.getIceServers(v)
              }),
              M = e => {
                Ke.off("p2p:dispose", j), Ke.off("p2p:answer", T), Ke.off("p2p:ice", P), a
                  .removeEventListener("inactive", L), i && i.close(), y.close(), e ? ("string" ==
                    typeof e && (e = new Error(e)), Ke.emit("p2p:dispose", {
                      to: o,
                      id: n,
                      error: e.message
                    }), console.error(e)) : Ke.emit("p2p:dispose", {
                    to: o,
                    id: n
                  }), "function" == typeof p && p({
                    id: n,
                    room: s,
                    user: c,
                    data: l,
                    error: e
                  })
              },
              j = e => {
                e && e.id === n && M(e.error)
              };
            Ke.on("p2p:dispose", j);
            var P = e => {
              e && e.id === n && e.candidate && y.addIceCandidate(e.candidate)
            };
            Ke.on("p2p:ice", P), y.addEventListener("iceconnectionstatechange", (e => {
              switch (e.target.iceConnectionState) {
              case "disconnected":
                M("ICE connection state is disconnected");
                break;
              case "failed":
                M("ICE connection state is failed")
              }
            })), y.addEventListener("icecandidate", (e => {
              e && e.candidate && Ke.emit("p2p:ice", {
                to: o,
                id: n,
                candidate: e.candidate
              })
            })), "function" == typeof y.createDataChannel && (i = y.createDataChannel(n));
            var T = e => {
              if (e && e.answer && e.id === n) {
                Ke.off("p2p:answer", T);
                var o = new RTCSessionDescription(e.answer);
                y.setRemoteDescription(o).then((() => {
                  ! function (e, t) {
                    if (t) "function" == typeof e.getSenders && "RTCRtpSender" in window &&
                      "getParameters" in window.RTCRtpSender.prototype && "setParameters" in
                      window.RTCRtpSender.prototype && e.getSenders().forEach((function (e) {
                        var r = t[e.track && e.track.kind];
                        if (r) {
                          var i = e.getParameters();
                          i.encodings || (i.encodings = []);
                          for (var n = 0; n < i.encodings.length; n++) {
                            var o = i.encodings[n];
                            o && (o.maxBitrate = 1e3 * r)
                          }
                          e.setParameters(i)
                        }
                      }))
                  }(y, {
                    audio: g,
                    video: f
                  }), t({
                    id: n,
                    room: s,
                    user: c,
                    data: l,
                    stream: a,
                    peer: y,
                    channel: i,
                    dispose: M
                  })
                })).catch((e => {
                  M(e), r(e)
                }))
              }
            };
            Ke.on("p2p:answer", T);
            var L = () => M();
            a.addEventListener("inactive", L), a.getTracks().forEach((e => y.addTrack(e, a))), y
              .createOffer({
                offerToReceiveAudio: !0,
                offerToReceiveVideo: !0,
                voiceActivityDetection: !0,
                iceRestart: !1
              }).then((e => {
                var t = g >>> 0,
                  r = f >>> 0,
                  i = e.sdp;
                return i = function (e, t) {
                    if (!t) return e;
                    var r = t.audio,
                      i = t.video,
                      n = "AS";
                    return "firefox" === Wt.browserDetails.browser && (r = 1e3 * (r >>> 0), i =
                        1e3 * (i >>> 0), n = "TIAS"), e = e.replace(/b=AS:.*\r\n/g, "").replace(
                        /b=TIAS:.*\r\n/g, ""), r && (e = e.replace(/m=audio (.*)\r\n/g,
                        "m=audio $1\r\nb=".concat(n, ":").concat(r, "\r\n"))), i && (e = e.replace(
                        /m=video (.*)\r\n/g, "m=video $1\r\nb=".concat(n, ":").concat(i, "\r\n"))),
                      e
                  }(i, u), i = $t(i, "audio", "opus/48000/2"), i = $t(i, "video", "H264/90000"), i =
                  $t(i, "video", "VP9/90000"), i = _t(i = $t(i, "video", "VP8/90000"),
                    "opus/48000/2", {
                      maxaveragebitrate: 1e3 * t,
                      maxplaybackrate: 1e3 * t,
                      stereo: 0
                    }), i = _t(i, "VP8/90000", {
                    "x-google-min-bitrate": r,
                    "x-google-max-bitrate": r
                  }), i = _t(i, "VP9/90000", {
                    "x-google-min-bitrate": r,
                    "x-google-max-bitrate": r
                  }), i = _t(i, "H264/90000", {
                    "max-br": r
                  }), e.sdp = i, y.setLocalDescription(e)
              })).then((() => {
                Ke.emit("p2p:offer", {
                  to: o,
                  id: n,
                  rid: s,
                  uid: c,
                  data: l,
                  offer: y.localDescription
                })
              })).catch((e => {
                M(e), r(e)
              }))
          }))
        }
        static createAnswer() {
          var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {};
          return new Promise(((t, r) => {
            var i, n = e.id,
              o = e.from,
              a = e.room,
              s = e.user,
              c = e.data,
              l = e.config,
              d = e.offer,
              u = e.ondata,
              p = e.ondispose,
              v = l.turnURI,
              m = new RTCPeerConnection({
                iceServers: er.getIceServers(v)
              }),
              h = e => {
                Ke.off("p2p:dispose", g), Ke.off("p2p:ice", b), i && i.close(), m.close(), e ? (
                  "string" == typeof e && (e = new Error(e)), Ke.emit("p2p:dispose", {
                    to: o,
                    id: n,
                    error: e.message
                  }), console.error(e)) : Ke.emit("p2p:dispose", {
                  to: o,
                  id: n
                }), "function" == typeof p && p({
                  id: n,
                  room: a,
                  user: s,
                  data: c,
                  error: e
                })
              },
              g = e => {
                e && e.id === n && h(e.error)
              };
            Ke.on("p2p:dispose", g);
            var b = e => {
              e && e.id === n && e.candidate && m.addIceCandidate(e.candidate)
            };
            Ke.on("p2p:ice", b), m.addEventListener("iceconnectionstatechange", (e => {
              switch (e.target.iceConnectionState) {
              case "disconnected":
                h("ICE connection state is disconnected");
                break;
              case "failed":
                h("ICE connection state is failed")
              }
            })), m.addEventListener("icecandidate", (e => {
              e && e.candidate && Ke.emit("p2p:ice", {
                to: o,
                id: n,
                candidate: e.candidate
              })
            })), m.addEventListener("datachannel", (e => {
              (i = e.channel).addEventListener("message", u)
            })), m.addEventListener("track", (e => {
              var r = e.streams[0];
              t({
                id: n,
                room: a,
                user: s,
                data: c,
                stream: r,
                peer: m,
                channel: i,
                dispose: h
              })
            }));
            var f = new RTCSessionDescription(d);
            m.setRemoteDescription(f).then((() => m.createAnswer())).then((e => m.setLocalDescription(
              e))).then((() => {
              Ke.emit("p2p:answer", {
                to: o,
                id: n,
                answer: m.localDescription
              })
            })).catch((e => {
              h(e), r(e)
            }))
          }))
        }
        static getIceServers(e) {
          if (!e) return [{
            urls: "stun:stun.l.google.com:19302"
          }];
          var t = xe(e),
            r = t.options || {},
            i = t.hosts || [],
            n = [];
          return (r.transport || "").split("+").forEach((e => {
            var o = {
              urls: i.map((r => {
                var i = e ? "?transport=".concat(e) : "";
                return "".concat(t.scheme, ":").concat(r.host || "127.0.0.1", ":").concat(r
                  .port || "3478").concat(t.endpoint || "").concat(i)
              })).sort((() => .5 - Math.random())).splice(0, r.quorum || 2)
            };
            t.username && (o.username = t.username), t.password && (o.credential = t.password), n.push(
              o)
          })), n
        }
        broadcast() {
          var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {},
            t = e.stream,
            r = e.room,
            i = e.user,
            n = e.data,
            o = e.bitrate;
          if (!this._streams[t.id]) {
            this._streams[t.id] = t;
            var a = this._config,
              s = {},
              c = () => {
                for (var e in s) {
                  var t = s[e];
                  if (delete s[e], "function" == typeof t) return setTimeout(t.bind(this, e), 0)
                }
              };
            this.bind("p2p:invoke", (e => {
              var l = e.from,
                d = e.id,
                u = e.rid,
                p = e.uid,
                v = [d, t.id].join("-");
              s[v] || r !== u || i === p || (s[v] = e => this._peers[e] ? c() : er.createOffer({
                from: l,
                id: e,
                room: r,
                user: i,
                data: n,
                stream: t,
                bitrate: o,
                config: a,
                ondispose: e => {
                  delete this._peers[e.id], this.dispatchEvent("stop", e)
                }
              }).then((e => (this._peers[e.id] = e, this.dispatchEvent("start", e), c()))).catch((
                e => (console.error(e), c()))), Object.keys(s).length > 1 || c())
            })), Ke.emit("p2p:broadcast", {
              to: r,
              rid: r,
              uid: i
            })
          }
        }
        listen() {
          var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {},
            t = e.room,
            r = e.user,
            i = e.ping,
            n = void 0 === i ? 3e4 : i,
            o = this._config,
            a = ke(),
            s = {},
            c = () => {
              for (var e in s) {
                var t = s[e];
                if (delete s[e], "function" == typeof t) return setTimeout(t.bind(this, e), 0)
              }
            };
          this.bind("p2p:offer", (e => {
            var i = e.from,
              n = e.id,
              a = e.rid,
              l = e.uid,
              d = e.data,
              u = e.offer;
            s[n] || t !== a || r === l || (s[n] = e => this._peers[e] ? c() : er.createAnswer({
              from: i,
              id: e,
              room: a,
              user: l,
              data: d,
              offer: u,
              config: o,
              ondata: e => {
                var t;
                try {
                  t = JSON.parse(e.data)
                } catch (r) {
                  t = e.data
                }
                this.dispatchEvent("data", t)
              },
              ondispose: e => {
                delete this._peers[e.id], this.dispatchEvent("stop", e)
              }
            }).then((e => (this._peers[e.id] = e, this.dispatchEvent("start", e), c()))).catch((e =>
              (console.error(e), c()))), Object.keys(s).length > 1 || c())
          })), this.bind("p2p:broadcast", (e => {
            var i = e.from,
              n = e.rid,
              o = e.uid;
            t === n && r !== o && Ke.emit("p2p:invoke", {
              to: i,
              id: a,
              rid: t,
              uid: r
            })
          })), Ke.emit("p2p:invoke", {
            to: t,
            id: a,
            rid: t,
            uid: r
          }), this._timer = setInterval((() => {
            Ke.emit("p2p:invoke", {
              to: t,
              id: a,
              rid: t,
              uid: r
            })
          }), n)
        }
        stop() {
          for (var e in clearInterval(this._timer), this._handlers) Ke.off(e, this._handlers[e]), delete this
            ._handlers[e];
          for (var t in this._peers) {
            var r = this._peers[t];
            delete this._peers[t], "function" == typeof r.dispose && r.dispose()
          }
          for (var i in this._streams) {
            var n = this._streams[i];
            delete this._streams[i], n.oninactive = null, n.getTracks().forEach((e => e.stop()))
          }
        }
        send(e) {
          for (var t in this._peers) {
            var r = this._peers[t].channel;
            if (r && "open" === r.readyState) {
              var i = void 0;
              try {
                i = JSON.stringify(e)
              } catch (t) {
                i = e
              }
              r.send(i)
            }
          }
        }
        bind(e, t) {
          e && t && (this._handlers[e] && Ke.off(e, this._handlers[e]), this._handlers[e] = t, Ke.on(e, this
            ._handlers[e]))
        }
        on(e, t) {
          e && t && (e = [].concat(e)).forEach((e => {
            this._events[e] || (this._events[e] = []), this._events[e].push(t)
          }))
        }
        off(e, t) {
          if (!e) return this._events = {};
          (e = [].concat(e)).forEach((e => {
            t || delete this._events[e];
            var r = this._events[e];
            if (r) {
              var i = r.indexOf(t);
              i > -1 && r.splice(i, 1)
            }
          }))
        }
        dispatchEvent(e, t) {
          var r = this._events[e];
          r && r.forEach((e => e.call(this, t)))
        }
        get config() {
          return this._config
        }
        set config(e) {
          this._config = e || {}
        }
        get streams() {
          return Object.keys(this._streams).map((e => this._streams[e]))
        }
        get peers() {
          return Object.keys(this._peers).map((e => this._peers[e]))
        }
        get audioEnabled() {
          var e = !1;
          e: for (var t in this._streams)
            for (var r = this._streams[t].getAudioTracks(), i = 0; i < r.length; i++)
              if (r[i].enabled) {
                e = !0;
                break e
              }
          return e
        }
        set audioEnabled(e) {
          for (var t in void 0 === e && (e = !0), this._streams)
            for (var r = this._streams[t].getAudioTracks(), i = 0; i < r.length; i++) r[i].enabled = e
        }
        get videoEnabled() {
          var e = !1;
          e: for (var t in this._streams)
            for (var r = this._streams[t].getVideoTracks(), i = 0; i < r.length; i++)
              if (r[i].enabled) {
                e = !0;
                break e
              }
          return e
        }
        set videoEnabled(e) {
          for (var t in void 0 === e && (e = !0), this._streams)
            for (var r = this._streams[t].getVideoTracks(), i = 0; i < r.length; i++) r[i].enabled = e
        }
        get enabled() {
          return this.audioEnabled || this.videoEnabled
        }
        set enabled(e) {
          void 0 === e && (e = !0), this.audioEnabled = e, this.videoEnabled = e
        }
      }
      var tr;
      class rr {
        constructor() {
          var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {};
          this._video = e.video, this._name = e.name || "record", this._duration = e.duration || 0, this
            ._jpegQuality = e.jpegQuality || .5, this._audioBitsPerSecond = e.audioBitsPerSecond || 16e3, this
            ._videoBitsPerSecond = e.videoBitsPerSecond || 1e5
        }
        start(e, t) {
          return new Promise(((r, i) => {
            if (this._started || this._recorder) return r();
            this._started = !0, this._timeout = setTimeout((() => {
              this._recorder = null, this._started = !1, i(new Error("Recorder not responding"))
            }), 1e4);
            try {
              var n, o, a;
              if (!rr.isSupported) throw Error("MediaRecorder is not supported");
              if (!(null !== (n = e = e || this._video) && void 0 !== n && n.srcObject || null !== (o =
                    e) && void 0 !== o && o.getVideoTracks || null !== (a = e) && void 0 !== a && a
                  .getAudioTracks)) throw Error("No video source");
              if (this._files = [], t && (this._name = t), this._video = e, e.srcObject) {
                if (!e.videoWidth || !e.videoHeight) throw Error("No video found");
                var s = Ce(e, {
                  quality: this._jpegQuality,
                  filename: "".concat(this._name, ".jpg")
                });
                this._files.push(s)
              }
              var c = e.srcObject || e,
                l = !!c.getAudioTracks && c.getAudioTracks().length > 0,
                d = !!c.getVideoTracks && c.getVideoTracks().length > 0,
                u = Wt.browserDetails.browser,
                p = [],
                v = "video/webm";
              switch (u) {
              case "firefox":
              case "chrome":
                v = d ? "video/webm" : "audio/webm", d && p.push("vp8"), l && p.push("opus");
                break;
              case "safari":
                v = d ? "video/mp4" : "audio/mp4", d && p.push("avc1.42001e"), l && p.push("mp4a.40.2")
              }
              this._mimeType = v;
              var m = new MediaRecorder(c, {
                mimeType: p.length > 0 ? "".concat(v, ";codecs=").concat(p.join(",")) : "".concat(
                  v),
                audioBitsPerSecond: this._audioBitsPerSecond,
                videoBitsPerSecond: this._videoBitsPerSecond
              });
              this._recorder = m, m.onerror = e => {
                this._recorder = null, this._started = !1, clearTimeout(this._timeout), i(e)
              };
              var h = v.match(/^\w+\/(\w+)/),
                g = h[0],
                b = h[1],
                f = "".concat(this._name, ".").concat(b);
              m.ondataavailable = e => {
                if (e.data && e.data.size) {
                  var t = new File([e.data], f, {
                    type: g
                  });
                  this._files.push(t)
                }
              }, m.onstart = () => {
                clearTimeout(this._timeout), r()
              }, m.start(), this._duration > 0 && (this._timer = setTimeout((() => this.stop()), 1e3 *
                this._duration))
            } catch (e) {
              this._recorder = null, this._started = !1, clearTimeout(this._timeout), i(e)
            }
          }))
        }
        stop() {
          return clearTimeout(this._timer), new Promise(((e, t) => {
            if (!this._started || !this._recorder) return e(this._files);
            var r = this._recorder;
            this._recorder = null, this._started = !1, this._timeout = setTimeout((() => {
              t(new Error("Recorder not responding"))
            }), 1e4);
            try {
              r.onerror = e => {
                clearTimeout(this._timeout), t(e)
              }, r.onstop = () => {
                clearTimeout(this._timeout), e(this._files)
              }, r.stop()
            } catch (e) {
              clearTimeout(this._timeout), t(e)
            }
          }))
        }
        get active() {
          var e;
          return this._started && "recording" === (null === (e = this._recorder) || void 0 === e ? void 0 : e
            .state)
        }
        get files() {
          return this._files || []
        }
        get video() {
          return this._video
        }
        static get isSupported() {
          return !!window.MediaRecorder
        }
      }
      var ir = {
        get: e => e ? e.split(".").reduce((function (e, t) {
          return e ? e[t] : e
        }), tr) : tr,
        sync: e => tr = e,
        usage() {
          if (tr) {
            var e = new Date,
              t = new Date(1e3 * tr.nbf),
              r = new Date(1e3 * tr.exp),
              i = Math.ceil(tr.volume || 0),
              n = Math.ceil(tr.used || 0) / i;
            (isNaN(n) || n > 1) && (n = 1);
            var o = (e.getTime() - t.getTime()) / (r.getTime() - t.getTime());
            return (isNaN(o) || o < 0 || o > 1) && (o = 1), tr.host !== location.host && (n = 1, o = 1), {
              usage: n,
              expires: o
            }
          }
        }
      };
      const nr = ir;
      var or, ar = {
        get: e => e && or ? e.split(".").reduce((function (e, t) {
          return e ? e[t] : e
        }), or) : or,
        filter(e) {
          if (Array.isArray(e) || (e = arguments), !e.length) return ar.get();
          for (var t = {}, r = 0, i = e.length; r < i; r++) {
            var n = e[r],
              o = ar.get(n);
            void 0 !== o && (t[n] = o)
          }
          return t
        },
        sync: e => or = e,
        start: () => ar.get("id") ? Ee("/api/room/start/".concat(ar.get("id")), {
          method: "POST"
        }).then((e => e.id ? or = e : or)) : new Promise(((e, t) => {
          var r = new Error("Session not found");
          r.code = "ERR_SESSION_NOT_FOUND", t(r)
        })),
        stop: () => ar.get("id") ? Ee("/api/room/stop/".concat(ar.get("id")), {
          method: "POST"
        }).then((e => e.id ? or = e : or)) : new Promise(((e, t) => {
          var r = new Error("Session not found");
          r.code = "ERR_SESSION_NOT_FOUND", t(r)
        })),
        update() {
          var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {};
          return ar.get("id") ? Ee("/api/room/update/".concat(ar.get("id")), {
            method: "POST",
            body: e
          }).then((e => e.id ? or = e : or)) : new Promise(((e, t) => {
            var r = new Error("Session not found");
            r.code = "ERR_SESSION_NOT_FOUND", t(r)
          }))
        },
        getAddons() {
          var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : [],
            t = ar.get("addons") || [];
          return e.filter((e => t.indexOf(e) >= 0))
        },
        hasAddon(e) {
          var t = ar.get("addons") || [];
          return [].concat(e).reduce(((e, r) => (t.indexOf(r) >= 0 && (e = !0), e)), !1)
        }
      };
      const sr = ar;
      var cr, lr = {
        get token() {
          return Ee.token
        },
        sync() {
          var e = (arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {}).token;
          return e && (Ee.token = e), Ee("/api/state").then((e => {
            if (!e) throw Error("Unauthorized");
            return nr.sync(e.license), l.sync(e.config), Re.sync(e.user), sr.sync(e.room), Ke.sync()
              .catch((() => {}))
          })).then((() => (cr = setInterval((() => lr.refresh()), 36e5), u.dispatchEvent(
          "session:refresh", {
            token: Ee.token
          }), {
            token: Ee.token
          }))).catch((e => {
            throw Ke.close(), e
          }))
        },
        login() {
          var e, t = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {},
            r = {
              method: "POST"
            };
          return "string" == typeof t.token ? (e = t.provider || "jwt", r.headers = {
            Authorization: "Bearer ".concat(t.token)
          }) : (e = t.provider || "login", r.body = t, Ee.token && (r.headers = {
            Authorization: "Bearer ".concat(Ee.token)
          })), Ee("/api/auth/".concat(e), r).then((function () {
            var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {};
            return lr.sync({
              token: e.token
            })
          }))
        },
        logout: () => (clearInterval(cr), Ee("/api/auth/logout", {
          method: "POST"
        }).then((() => {
          var e = Re.get("referrer");
          return Re.sync(null), sr.sync(null), l.sync(null), nr.sync(null), Ke.close(), Ee.token =
          "", {
            referrer: e
          }
        }))),
        refresh: () => Ee("/api/auth").then((e => (e && e.token && (Ee.token = e.token, u.dispatchEvent(
          "session:refresh", e)), e))),
        qrcode() {
          var e = (arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {}).redirect;
          return Ee("/api/auth/qrcode", {
            method: "POST",
            body: {
              redirect: void 0 === e ? "" : e,
              origin: Ee.url || location.origin
            }
          })
        }
      };
      const dr = lr;
  
      function ur(e, t) {
        var r = Object.keys(e);
        if (Object.getOwnPropertySymbols) {
          var i = Object.getOwnPropertySymbols(e);
          t && (i = i.filter((function (t) {
            return Object.getOwnPropertyDescriptor(e, t).enumerable
          }))), r.push.apply(r, i)
        }
        return r
      }
  
      function pr(e) {
        for (var t = 1; t < arguments.length; t++) {
          var r = null != arguments[t] ? arguments[t] : {};
          t % 2 ? ur(Object(r), !0).forEach((function (t) {
            vr(e, t, r[t])
          })) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object
            .getOwnPropertyDescriptors(r)) : ur(Object(r)).forEach((function (t) {
            Object.defineProperty(e, t, Object.getOwnPropertyDescriptor(r, t))
          }))
        }
        return e
      }
  
      function vr(e, t, r) {
        return t = function (e) {
          var t = function (e, t) {
            if ("object" != typeof e || null === e) return e;
            var r = e[Symbol.toPrimitive];
            if (void 0 !== r) {
              var i = r.call(e, t || "default");
              if ("object" != typeof i) return i;
              throw new TypeError("@@toPrimitive must return a primitive value.")
            }
            return ("string" === t ? String : Number)(e)
          }(e, "string");
          return "symbol" == typeof t ? t : String(t)
        }(t), t in e ? Object.defineProperty(e, t, {
          value: r,
          enumerable: !0,
          configurable: !0,
          writable: !0
        }) : e[t] = r, e
      }
      var mr;
      const hr = {
        get active() {
          return !!mr
        },
        start: (e, t) => new Promise((r => {
          if (mr) return r();
          var i = pr(pr({
            interval: 1,
            skip: 0,
            offsetX: 50,
            offsetY: 85
          }, l.get("tracker.browser")), t);
          ! function (e, t) {
            var r = e.interval,
              i = e.skip,
              n = {
                supported: !0,
                focused: !0,
                maximized: !0
              },
              o = 0,
              a = !1,
              s = !1;
            mr = setInterval((function () {
              if (!s) {
                if (o < i) return o++;
                s = !0, ! function () {
                  var e = Wt.browserDetails,
                    t = e.browser,
                    r = e.version,
                    i = Zt();
                  return !(i && /MiuiBrowser/.test(navigator.userAgent) || !("chrome" === t &&
                      r >= 72 || "firefox" === t && r >= 66 || "safari" === t && r >= 13) && !
                    ("safari" === t && r >= 12 && i) && !("firefox" === t && r >= 52 && Ft()))
                }() || sr.hasAddon("record") && !rr.isSupported || !sr.hasAddon("mobile") &&
                Zt() ? n.supported = !1 : n.supported = !0;
                var r = document.hasFocus();
                a ? n.focused = r : r && (a = !0), screen.availWidth - window.outerWidth <= e
                  .offsetX && screen.availHeight - window.outerHeight <= e.offsetY ? n
                  .maximized = !0 : Zt() || (n.maximized = !1), s = !1, setTimeout(t.bind(null,
                    pr({}, n)), 0)
              }
            }), 1e3 * r)
          }(i, e), r(i)
        })),
        stop: () => new Promise((e => {
          if (!mr) return e();
          clearInterval(mr), mr = null, e()
        }))
      };
  
      function gr(e, t) {
        t = Object.assign({
          shiftfactor: .1,
          scalefactor: 1.1,
          initialsize: .1,
          rotation: [0, 30, 330],
          threshold: .2,
          memory: 1
        }, t || {});
        var r = function (e) {
            var t = new DataView(new ArrayBuffer(4)),
              r = 8;
            t.setUint8(0, e[r + 0]), t.setUint8(1, e[r + 1]), t.setUint8(2, e[r + 2]), t.setUint8(3, e[r + 3]);
            var i = t.getInt32(0, !0),
              n = Math.pow(2, i) >> 0;
            r += 4, t.setUint8(0, e[r + 0]), t.setUint8(1, e[r + 1]), t.setUint8(2, e[r + 2]), t.setUint8(3, e[
              r + 3]);
            var o = t.getInt32(0, !0);
            r += 4;
            for (var a = [], s = [], c = [], l = 0; l < o; ++l) {
              Array.prototype.push.apply(a, [0, 0, 0, 0]), Array.prototype.push.apply(a, e.slice(r, r + 4 * n -
                4)), r = r + 4 * n - 4;
              for (var d = 0; d < n; ++d) t.setUint8(0, e[r + 0]), t.setUint8(1, e[r + 1]), t.setUint8(2, e[r +
                2]), t.setUint8(3, e[r + 3]), s.push(t.getFloat32(0, !0)), r += 4;
              t.setUint8(0, e[r + 0]), t.setUint8(1, e[r + 1]), t.setUint8(2, e[r + 2]), t.setUint8(3, e[r +
                3]), c.push(t.getFloat32(0, !0)), r += 4
            }
            for (var u = [], p = [], v = 0; v < 360; v++) {
              var m = v * Math.PI / 180;
              u[v] = 256 * Math.cos(m), p[v] = 256 * Math.sin(m)
            }
            return function (e, t, r, l, d, v) {
              e <<= 16, t <<= 16;
              for (var m = 0, h = 0, g = l * p[r |= 0], b = l * u[r], f = 0; f < o; ++f) {
                for (var y = 1, M = 0; M < i; ++M) {
                  var j = m + 4 * y,
                    P = a[j + 0],
                    T = a[j + 1],
                    L = a[j + 2],
                    A = a[j + 3],
                    w = e + b * L - g * A >> 16,
                    k = t + g * L + b * A >> 16;
                  y = 2 * y + (d[(e + b * P - g * T >> 16) * v + (t + g * P + b * T >> 16)] <= d[w * v + k])
                }
                if ((h += s[n * f + y - n]) <= c[f]) return -1;
                m += 4 * n
              }
              return h - c[o - 1]
            }
          }(new Int8Array(e)),
          i = function (e) {
            for (var t = 0, r = [], i = 0; i < e; ++i) r.push([]);
            return function (e) {
              r[t] = e, t = (t + 1) % r.length, e = [];
              for (var i = 0; i < r.length; ++i) e = e.concat(r[i]);
              return e
            }
          }(t.memory);
  
        function n(e, t) {
          var r = e[0],
            i = e[1],
            n = e[2],
            o = t[0],
            a = t[1],
            s = t[2],
            c = Math.max(0, Math.min(r + n / 2, o + s / 2) - Math.max(r - n / 2, o - s / 2)),
            l = Math.max(0, Math.min(i + n / 2, a + s / 2) - Math.max(i - n / 2, a - s / 2)),
            d = Math.min(n, s);
          return c * l / (d * d)
        }
        return function (e) {
          var o = e.data,
            a = e.width,
            s = e.height,
            c = function (e, t, r, i) {
              var n = e.length >> 2,
                o = i ? new Uint32Array(n) : new Uint8Array(n),
                a = new Uint32Array(e.buffer || new Uint8Array(e).buffer),
                s = 0,
                c = 0,
                l = 0;
              if (i)
                for (; s < n;) l = 13933 * ((c = a[s]) >>> 16 & 255) + 46871 * (c >>> 8 & 255) + 4732 * (255 &
                  c) >>> 16, o[s++] = 65793 * l | 4278190080 & c;
              else
                for (; s < n;) l = 13933 * ((c = a[s]) >>> 16 & 255) + 46871 * (c >>> 8 & 255) + 4732 * (255 &
                  c) >>> 16, o[s++] = l;
              return new Uint8ClampedArray(o.buffer)
            }(o),
            l = t,
            d = l.shiftfactor,
            u = l.scalefactor,
            p = l.initialsize,
            v = l.rotation,
            m = l.threshold,
            h = function (e, t, r, i, n, o, a, s) {
              s = s ? [].concat(s) : [0];
              var c = a * Math.sqrt(t * r) | 0,
                l = Math.min(t, r),
                d = [];
              for (; l >= c;) {
                for (var u = n * l + 1 >> 0, p = l / 2 + 1 >> 0, v = p; v < r - p; v += u)
                  for (var m = p; m < t - p; m += u)
                    for (var h = 0; h < s.length; h++) {
                      var g = s[h],
                        b = i(v, m, g, l, e, t);
                      b > 0 && d.push([v, m, l, b, g])
                    }
                l /= o
              }
              return d
            }(c, a, s, r, d, u, p, v);
          return h = function (e, t) {
            e.sort((function (e, t) {
              return t[3] - e[3]
            }));
            for (var r = [], i = [], o = 0; o < e.length; o++)
              if (!r[o]) {
                for (var a = e[o][0], s = e[o][1], c = e[o][2], l = e[o][3], d = e[o][4], u = 1, p = o +
                  1; p < e.length; p++) r[p] || n(e[o], e[p]) > t && (r[p] = !0, a += e[p][0], s += e[p][1],
                  c += e[p][2], l += e[p][3], u++);
                i.push({
                  r: a / u | 0,
                  c: s / u | 0,
                  s: c / u | 0,
                  q: l,
                  a: d
                })
              } return i
          }(i(h), m), h
        }
      }
  
      function br(e, t, r) {
        var i = "(function(){".concat(gr.toString(), ";var detect=").concat(gr.name, "([").concat(new Int8Array(
            e).toString(), "],").concat(JSON.stringify(t || {}),
            ");onmessage=function(e){postMessage(detect(e.data));};})();"),
          n = new Blob([i]),
          o = URL.createObjectURL(n, {
            type: "application/javascript; charset=utf-8"
          }),
          a = new Worker(o);
        return a.onmessage = function (e) {
            r(e.data)
          },
          function (e) {
            a.postMessage(e)
          }
      }
  
      function fr(e, t) {
        var r = Object.keys(e);
        if (Object.getOwnPropertySymbols) {
          var i = Object.getOwnPropertySymbols(e);
          t && (i = i.filter((function (t) {
            return Object.getOwnPropertyDescriptor(e, t).enumerable
          }))), r.push.apply(r, i)
        }
        return r
      }
  
      function yr(e) {
        for (var t = 1; t < arguments.length; t++) {
          var r = null != arguments[t] ? arguments[t] : {};
          t % 2 ? fr(Object(r), !0).forEach((function (t) {
            Mr(e, t, r[t])
          })) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object
            .getOwnPropertyDescriptors(r)) : fr(Object(r)).forEach((function (t) {
            Object.defineProperty(e, t, Object.getOwnPropertyDescriptor(r, t))
          }))
        }
        return e
      }
  
      function Mr(e, t, r) {
        return t = function (e) {
          var t = function (e, t) {
            if ("object" != typeof e || null === e) return e;
            var r = e[Symbol.toPrimitive];
            if (void 0 !== r) {
              var i = r.call(e, t || "default");
              if ("object" != typeof i) return i;
              throw new TypeError("@@toPrimitive must return a primitive value.")
            }
            return ("string" === t ? String : Number)(e)
          }(e, "string");
          return "symbol" == typeof t ? t : String(t)
        }(t), t in e ? Object.defineProperty(e, t, {
          value: r,
          enumerable: !0,
          configurable: !0,
          writable: !0
        }) : e[t] = r, e
      }
      var jr, Pr, Tr;
      const Lr = {
        get active() {
          return !!jr
        },
        start: (e, t, r) => new Promise((i => {
          if (!e || jr) return i();
          var n = yr(yr({
            interval: 3,
            count: 20,
            threshold: 20,
            quality: .9
          }, l.get("tracker.camera")), r);
          if (e instanceof HTMLVideoElement == !1) {
            var o = document.createElement("video");
            o.autoplay = !0, o.playsinline = !0, o.muted = !0, o.setAttribute("autoplay", ""), o
              .setAttribute("playsinline", ""), o.setAttribute("muted", ""), void 0 !== o.srcObject ? o
              .srcObject = e : (Pr = URL.createObjectURL(e), o.src = Pr), e = o
          }
          Ar().then((r => {
            ! function (e, t, r, i) {
              var n, o, a, s = r.interval,
                c = r.count,
                l = r.threshold,
                d = r.quality,
                u = r.detection,
                p = [],
                v = br(t, u, (e => {
                  if (e = e.filter((e => e.q > l)), 1 === e.length && p.push({
                      image: n.canvas,
                      det: e[0]
                    }), p.length >= c) {
                    var t = p.sort(((e, t) => t.det.q - e.det.q))[0] || {},
                      r = kr(t.image, t.det, d);
                    p = [], Nr({
                      type: "face",
                      file: De(r, "face.jpg"),
                      ref: sr.get("student.face")
                    }).then((e => {
                      var t = e.metadata || {},
                        n = t.distance,
                        o = t.threshold,
                        a = t.similar,
                        s = t.verified,
                        c = {
                          id: e.id,
                          dataUrl: r,
                          distance: n,
                          threshold: o,
                          similar: a,
                          verified: s
                        };
                      Object.defineProperty(c, "file", {
                        get: function () {
                          return De(this.dataUrl, "face.jpg")
                        },
                        enumerable: !0,
                        configurable: !0
                      }), setTimeout(i.bind(null, c), 0)
                    }))
                  }
                  setTimeout(i.bind(null, e), 0), a = !1
                }));
              jr = setInterval((function () {
                if (!a) {
                  if (a = !0, !e.videoWidth || !e.videoHeight) return a = !1, setTimeout(i
                    .bind(null, !1), 0);
                  if (e.paused) {
                    var t = e.play();
                    t && "undefined" != typeof Promise && t instanceof Promise && t.catch((
                      function () {}))
                  }
                  var r = (n = wr(e, e.videoWidth, e.videoHeight)).getImageData(0, 0, n
                    .canvas.width, n.canvas.height);
                  if (function () {
                      var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[
                        0] : [],
                        t = arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] :
                        [],
                        r = !0,
                        i = e.length;
                      t.length > e.length && (i = t.length);
                      for (var n = 0; n < i; n++)
                        if (e[n] !== t[n]) {
                          r = !1;
                          break
                        } return r
                    }(o, r.data) || function (e) {
                      var t;
                      if (!e) return !1;
                      for (var r = (null == e ? void 0 : e.getVideoTracks()) || [], i =
                          null === (t = r[0]) || void 0 === t ? void 0 : t.label, n = 0,
                          o = [/AlterCam Virtual Camera/i, /CyberLink YouCam/i,
                            /DCC Virtual Camera/i, /e2eSoft VCam/i,
                            /EƖgato Virtual Camera/i, /FineShare FineCam/i, /Logi Capture/i,
                            /ManyCam Virtual Webcam/i, /OBS Virtual Camera/i,
                            /SplitCam Video Driver/i
                          ]; n < o.length; n++) {
                        if (o[n].test(i)) return !0
                      }
                      return !1
                    }(e.srcObject)) return a = !1, setTimeout(i.bind(null, !1), 0);
                  o = r.data, v(r)
                }
              }), 1e3 * s)
            }(e, r, n, t)
          })), i(n)
        })),
        stop: () => new Promise((e => {
          if (!jr) return e();
          clearInterval(jr), jr = null, Pr && (URL.revokeObjectURL(Pr), Pr = null), e()
        })),
        recognize(e, t) {
          var r = t || {},
            i = r.width,
            n = r.height,
            o = r.type,
            a = l.get("tracker.camera") || {},
            s = a.detection,
            c = a.threshold,
            d = void 0 === c ? 20 : c,
            u = a.quality,
            p = void 0 === u ? .9 : u;
          return new Promise(((t, r) => {
            var a = i || e.videoWidth || e.naturalWidth || e.width,
              c = n || e.videoHeight || e.naturalHeight || e.height,
              l = wr(e, a, c);
            if ("passport" === o) {
              var u = l.canvas.toDataURL("image/jpeg", p);
              return Nr({
                type: o,
                file: De(u, "passport.jpg"),
                ref: Re.get("passport"),
                nickname: sr.hasAddon("name") && Re.get("nickname")
              }).then((e => {
                var r = e.metadata || {},
                  i = r.distance,
                  n = r.threshold,
                  o = r.verified;
                t({
                  id: e.id,
                  dataUrl: u,
                  distance: i,
                  threshold: n,
                  verified: o
                })
              })).catch(r)
            }
            if ("face" === o) return Ar().then((e => {
              var i = br(e, s, (e => {
                if (e = e.filter((e => e.q > d)), e.length < 1) return r(new Error(
                  "Face not found"));
                if (e.length > 1) return r(new Error("Several faces were found"));
                var i = kr(l.canvas, e[0], p);
                return Nr({
                  type: o,
                  file: De(i, "face.jpg"),
                  ref: Re.get("face")
                }).then((e => {
                  var r = e.metadata || {},
                    n = r.distance,
                    o = r.threshold,
                    a = r.similar,
                    s = r.verified;
                  t({
                    id: e.id,
                    dataUrl: i,
                    distance: n,
                    threshold: o,
                    similar: a,
                    verified: s
                  })
                })).catch(r)
              }));
              i(l.getImageData(0, 0, l.canvas.width, l.canvas.height))
            }));
            var v = l.canvas.toDataURL("image/jpeg");
            return Nr({
              type: o,
              file: De(v, "extrapage.jpg")
            }).then((e => {
              t({
                id: e.id,
                dataUrl: v
              })
            })).catch(r)
          }))
        }
      };
  
      function Ar() {
        return Tr ? new Promise((e => e(Tr))) : (e = Ie(
          "data:application/octet-stream;base64,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"
          ), new Promise(((t, r) => {
          var i = new FileReader;
          i.readAsArrayBuffer(e), i.onload = function () {
            t(i.result)
          }, i.onerror = function () {
            r(i.error)
          }
        }))).then((e => Tr = e));
        var e
      }
  
      function wr(e, t, r, i, n) {
        var o = document.createElement("canvas"),
          a = o.getContext("2d");
        return o.width = t, o.height = r, i >= 0 && n >= 0 ? a.drawImage(e, i, n, t, r, 0, 0, t, r) : a
          .drawImage(e, 0, 0, t, r), a
      }
  
      function kr(e, t, r) {
        var i = arguments.length > 3 && void 0 !== arguments[3] ? arguments[3] : 280,
          n = arguments.length > 4 && void 0 !== arguments[4] ? arguments[4] : 320,
          o = t.c,
          a = t.r,
          s = t.s,
          c = .5 * i / s,
          l = .5 * n / s,
          d = function (e, t, r, i, n) {
            var o = document.createElement("canvas"),
              a = o.getContext("2d"),
              s = t * n,
              c = r * n;
            return o.width = Math.round(e.width * n), o.height = Math.round(e.height * n), a.save(), a
              .clearRect(0, 0, o.width, o.height), a.translate(s, c), a.rotate(-i * Math.PI / 180), a.drawImage(
                e, -s, -c, o.width, o.height), a.restore(), a
          }(e, o, a, -t.a, c),
          u = ~~(s * c * 2),
          p = ~~(s * l * 2),
          v = ~~(o * c - u / 2),
          m = ~~(a * l - p / 1.5);
        return v < 0 && (v = 0), m < 0 && (m = 0), (d = wr(d.canvas, u, p, v, m)).canvas.toDataURL("image/jpeg",
          r)
      }
  
      function Nr(e) {
        var t = e.file,
          r = e.type,
          i = e.ref,
          n = e.nickname;
        return Ee("/api/storage?type=".concat(r || "", "&ref=").concat(i || ""), {
          headers: "passport" === r && n ? {
            "x-passport-name": encodeURIComponent(n)
          } : {},
          body: t
        })
      }
  
      function Ir(e, t) {
        var r = Object.keys(e);
        if (Object.getOwnPropertySymbols) {
          var i = Object.getOwnPropertySymbols(e);
          t && (i = i.filter((function (t) {
            return Object.getOwnPropertyDescriptor(e, t).enumerable
          }))), r.push.apply(r, i)
        }
        return r
      }
  
      function Dr(e) {
        for (var t = 1; t < arguments.length; t++) {
          var r = null != arguments[t] ? arguments[t] : {};
          t % 2 ? Ir(Object(r), !0).forEach((function (t) {
            Cr(e, t, r[t])
          })) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object
            .getOwnPropertyDescriptors(r)) : Ir(Object(r)).forEach((function (t) {
            Object.defineProperty(e, t, Object.getOwnPropertyDescriptor(r, t))
          }))
        }
        return e
      }
  
      function Cr(e, t, r) {
        return t = function (e) {
          var t = function (e, t) {
            if ("object" != typeof e || null === e) return e;
            var r = e[Symbol.toPrimitive];
            if (void 0 !== r) {
              var i = r.call(e, t || "default");
              if ("object" != typeof i) return i;
              throw new TypeError("@@toPrimitive must return a primitive value.")
            }
            return ("string" === t ? String : Number)(e)
          }(e, "string");
          return "symbol" == typeof t ? t : String(t)
        }(t), t in e ? Object.defineProperty(e, t, {
          value: r,
          enumerable: !0,
          configurable: !0,
          writable: !0
        }) : e[t] = r, e
      }
      var zr, xr;
      const Er = {
        get active() {
          return !!xr
        },
        start: (e, t, r) => new Promise((i => {
          if (!e || zr || xr) return i();
          var n = Dr(Dr({
            interval: 1,
            timeout: 30,
            skip: 10,
            minFreq: 300,
            maxFreq: 3e3,
            threshold: .8,
            mindB: -59
          }, l.get("tracker.microphone")), r);
          ! function (e, t, r) {
            var i, n, o = t.threshold,
              a = t.mindB,
              s = t.minFreq,
              c = t.maxFreq,
              l = t.timeout,
              d = t.skip,
              u = t.interval,
              p = !1,
              v = !1,
              m = 0,
              h = (zr = new(window.AudioContext || window.webkitAudioContext)).createAnalyser(),
              g = 2048;
            h.minDecibels = -100, h.maxDecibels = -30, h.smoothingTimeConstant = .2, h.fftSize = g;
            var b, f, y = zr.createScriptProcessor(g, 1, 1);
            h.connect(y), y.connect(zr.destination), y.onaudioprocess = function (e) {
              if (!(e.playbackTime < d)) {
                var t = new Uint8Array(h.frequencyBinCount);
                h.getByteFrequencyData(t);
                var r = function (e, t, r, i, n) {
                  for (var o = t.context.sampleRate, a = t.frequencyBinCount, s = Or(i, o, a), c =
                      Or(n, o, a), l = 0; s < c; s++) r[s] > l && (l = r[s]);
                  return Sr(l / e)
                }(255, h, t, s, c);
                r > -1 / 0 && (i = Rr(i, r, .1), n = Rr(n, r * o, .001), i > n && (p = !0));
                var u = function (e) {
                  for (var t = -1 / 0, r = e.numberOfChannels, i = 0; i < r; i++) {
                    var n = Sr(e.getChannelData(i));
                    n > t && (t = n)
                  }
                  return t
                }(e.inputBuffer);
                (u > a || p) && (m = e.playbackTime), e.playbackTime - m > l && (v = !0)
              }
            }, e instanceof HTMLMediaElement == !1 && (f = e).getAudioTracks().length > 0 && (b = zr
              .createMediaStreamSource(e)).connect(h);
            xr = setInterval((function () {
              "running" !== zr.state ? zr.resume() : e.srcObject && e.srcObject !== f && (f = e
                .srcObject, b && b.disconnect(), f.getAudioTracks().length > 0 && (b = zr
                  .createMediaStreamSource(f)).connect(h)), setTimeout(r.bind(null, {
                muted: v,
                voiced: p
              }), 0), v = p = !1
            }), 1e3 * u)
          }(e, n, t), i(n)
        })),
        stop: () => new Promise((e => {
          if (!xr) return e();
          clearInterval(xr), xr = null, zr && ("function" == typeof zr.close && zr.close(), zr = null),
            e()
        }))
      };
  
      function Sr(e) {
        var t = 0;
        "number" == typeof e && (e = [].concat(e));
        for (var r = e.length, i = 0; i < r; i++) t += Math.abs(e[i]);
        var n = Math.sqrt(t / r);
        return 20 * Math.log(n) / Math.LN10
      }
  
      function Or(e, t, r) {
        var i = t / 2;
        return function (e, t, r) {
          return t < r ? e < t ? t : e > r ? r : e : e < r ? r : e > t ? t : e
        }(Math.round(e / i * r), 0, r)
      }
  
      function Rr(e, t) {
        var r = arguments.length > 2 && void 0 !== arguments[2] ? arguments[2] : .1;
        return e ? r * t + (1 - r) * e : t
      }
  
      function Qr(e, t) {
        var r = Object.keys(e);
        if (Object.getOwnPropertySymbols) {
          var i = Object.getOwnPropertySymbols(e);
          t && (i = i.filter((function (t) {
            return Object.getOwnPropertyDescriptor(e, t).enumerable
          }))), r.push.apply(r, i)
        }
        return r
      }
  
      function Yr(e) {
        for (var t = 1; t < arguments.length; t++) {
          var r = null != arguments[t] ? arguments[t] : {};
          t % 2 ? Qr(Object(r), !0).forEach((function (t) {
            Ur(e, t, r[t])
          })) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object
            .getOwnPropertyDescriptors(r)) : Qr(Object(r)).forEach((function (t) {
            Object.defineProperty(e, t, Object.getOwnPropertyDescriptor(r, t))
          }))
        }
        return e
      }
  
      function Ur(e, t, r) {
        return t = function (e) {
          var t = function (e, t) {
            if ("object" != typeof e || null === e) return e;
            var r = e[Symbol.toPrimitive];
            if (void 0 !== r) {
              var i = r.call(e, t || "default");
              if ("object" != typeof i) return i;
              throw new TypeError("@@toPrimitive must return a primitive value.")
            }
            return ("string" === t ? String : Number)(e)
          }(e, "string");
          return "symbol" == typeof t ? t : String(t)
        }(t), t in e ? Object.defineProperty(e, t, {
          value: r,
          enumerable: !0,
          configurable: !0,
          writable: !0
        }) : e[t] = r, e
      }
      var Gr, Br;
      const Kr = {
        get active() {
          return !!Gr
        },
        start: (e, t, r) => new Promise((i => {
          if (!e || Gr) return i();
          if (sr.hasAddon("mobile") && Zt()) return i();
          var n = Yr(Yr({
            interval: 5,
            skip: 6,
            diff: .1
          }, l.get("tracker.screen")), r);
          if (e instanceof HTMLVideoElement == !1) {
            var o = document.createElement("video");
            o.autoplay = !0, o.playsinline = !0, o.muted = !0, o.setAttribute("autoplay", ""), o
              .setAttribute("playsinline", ""), o.setAttribute("muted", ""), void 0 !== o.srcObject ? o
              .srcObject = e : (Br = URL.createObjectURL(e), o.src = Br), e = o
          }! function (e, t, r) {
            var i = t.interval,
              n = t.skip,
              o = t.diff,
              a = {
                captured: !0,
                natural: !0,
                single: !0
              },
              s = document.createElement("canvas"),
              c = s.getContext("2d"),
              l = function (e) {
                s.width = e.videoWidth, s.height = e.videoHeight, c.drawImage(e, 0, 0, s.width, s
                  .height);
                for (var t = c.getImageData(0, 0, s.width, s.height).data, r = 0, i = 0; i < t
                  .length; i += 4)
                  if ((r += t[i] + t[i + 1] + t[i + 2]) > 0) return !1;
                return !0
              },
              d = function () {
                var t, r;
                return /screen|monitor/i.test(null === (t = e.srcObject) || void 0 === t || null === (
                  r = t.getVideoTracks()[0]) || void 0 === r ? void 0 : r.label)
              },
              u = function (e) {
                var t = e.videoWidth,
                  r = e.videoHeight;
                return Math.abs(t / r - screen.width / screen.height) < o || /Mac OS/.test(navigator
                  .userAgent) && d()
              },
              p = 0,
              v = !1;
            Gr = setInterval((function () {
              if (!v) {
                if (p < n) return p++;
                v = !0;
                var t = e ? e.videoWidth : 0,
                  i = e ? e.videoHeight : 0;
                if (t > 0 && i > 0) {
                  if (e.paused) {
                    var o = e.play();
                    o && "undefined" != typeof Promise && o instanceof Promise && o.catch((
                      function () {}))
                  }
                  a.captured = !l(e), a.natural = u(e)
                } else a.captured = !1, a.natural = !0;
                "function" != typeof window.getScreenDetails || Ft() || Zt() || window
                  .getScreenDetails().then((e => {
                    var t = e.screens;
                    a.single = t.length < 2
                  })).catch((e => {
                    a.single = !1, console.error(e)
                  })), v = !1, setTimeout(r.bind(null, Yr({}, a)), 0)
              }
            }), 1e3 * i)
          }(e, n, t), i(n)
        })),
        stop: () => new Promise((e => {
          if (!Gr) return e();
          clearInterval(Gr), Gr = null, Br && (URL.revokeObjectURL(Br), Br = null), e()
        }))
      };
  
      function Hr(e, t) {
        var r = Object.keys(e);
        if (Object.getOwnPropertySymbols) {
          var i = Object.getOwnPropertySymbols(e);
          t && (i = i.filter((function (t) {
            return Object.getOwnPropertyDescriptor(e, t).enumerable
          }))), r.push.apply(r, i)
        }
        return r
      }
  
      function qr(e) {
        for (var t = 1; t < arguments.length; t++) {
          var r = null != arguments[t] ? arguments[t] : {};
          t % 2 ? Hr(Object(r), !0).forEach((function (t) {
            Wr(e, t, r[t])
          })) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object
            .getOwnPropertyDescriptors(r)) : Hr(Object(r)).forEach((function (t) {
            Object.defineProperty(e, t, Object.getOwnPropertyDescriptor(r, t))
          }))
        }
        return e
      }
  
      function Wr(e, t, r) {
        return t = function (e) {
          var t = function (e, t) {
            if ("object" != typeof e || null === e) return e;
            var r = e[Symbol.toPrimitive];
            if (void 0 !== r) {
              var i = r.call(e, t || "default");
              if ("object" != typeof i) return i;
              throw new TypeError("@@toPrimitive must return a primitive value.")
            }
            return ("string" === t ? String : Number)(e)
          }(e, "string");
          return "symbol" == typeof t ? t : String(t)
        }(t), t in e ? Object.defineProperty(e, t, {
          value: r,
          enumerable: !0,
          configurable: !0,
          writable: !0
        }) : e[t] = r, e
      }
      var Vr, Zr;
      const Fr = {
        get active() {
          return !!Vr
        },
        start: (e, t) => new Promise((r => {
          if (Vr) return r();
          var i = qr(qr({
            interval: 5
          }, l.get("tracker.network")), t);
          Zr = Date.now(), Ke.on("userdata", Jr), Vr = setInterval((function () {
            setTimeout(e.bind(null, {
              connected: Ke.connected,
              mobile: !sr.hasAddon("qrcode") || Date.now() - Zr < 6e4
            }), 0)
          }), 1e3 * i.interval), r(i)
        })),
        stop: () => new Promise((e => {
          if (!Vr) return e();
          clearInterval(Vr), Vr = null, Ke.off("userdata", Jr), e()
        }))
      };
  
      function Jr(e) {
        e && "mobile" === e.event && (Zr = Date.now())
      }
  
      function Xr(e, t) {
        return function (e) {
          if (Array.isArray(e)) return e
        }(e) || function (e, t) {
          var r = null == e ? null : "undefined" != typeof Symbol && e[Symbol.iterator] || e["@@iterator"];
          if (null != r) {
            var i, n, o, a, s = [],
              c = !0,
              l = !1;
            try {
              if (o = (r = r.call(e)).next, 0 === t) {
                if (Object(r) !== r) return;
                c = !1
              } else
                for (; !(c = (i = o.call(r)).done) && (s.push(i.value), s.length !== t); c = !0);
            } catch (e) {
              l = !0, n = e
            } finally {
              try {
                if (!c && null != r.return && (a = r.return(), Object(a) !== a)) return
              } finally {
                if (l) throw n
              }
            }
            return s
          }
        }(e, t) || function (e, t) {
          if (!e) return;
          if ("string" == typeof e) return _r(e, t);
          var r = Object.prototype.toString.call(e).slice(8, -1);
          "Object" === r && e.constructor && (r = e.constructor.name);
          if ("Map" === r || "Set" === r) return Array.from(e);
          if ("Arguments" === r || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)) return _r(e, t)
        }(e, t) || function () {
          throw new TypeError(
            "Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."
            )
        }()
      }
  
      function _r(e, t) {
        (null == t || t > e.length) && (t = e.length);
        for (var r = 0, i = new Array(t); r < t; r++) i[r] = e[r];
        return i
      }
  
      function $r(e, t) {
        var r = Object.keys(e);
        if (Object.getOwnPropertySymbols) {
          var i = Object.getOwnPropertySymbols(e);
          t && (i = i.filter((function (t) {
            return Object.getOwnPropertyDescriptor(e, t).enumerable
          }))), r.push.apply(r, i)
        }
        return r
      }
  
      function ei(e) {
        for (var t = 1; t < arguments.length; t++) {
          var r = null != arguments[t] ? arguments[t] : {};
          t % 2 ? $r(Object(r), !0).forEach((function (t) {
            ti(e, t, r[t])
          })) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object
            .getOwnPropertyDescriptors(r)) : $r(Object(r)).forEach((function (t) {
            Object.defineProperty(e, t, Object.getOwnPropertyDescriptor(r, t))
          }))
        }
        return e
      }
  
      function ti(e, t, r) {
        return t = function (e) {
          var t = function (e, t) {
            if ("object" != typeof e || null === e) return e;
            var r = e[Symbol.toPrimitive];
            if (void 0 !== r) {
              var i = r.call(e, t || "default");
              if ("object" != typeof i) return i;
              throw new TypeError("@@toPrimitive must return a primitive value.")
            }
            return ("string" === t ? String : Number)(e)
          }(e, "string");
          return "symbol" == typeof t ? t : String(t)
        }(t), t in e ? Object.defineProperty(e, t, {
          value: r,
          enumerable: !0,
          configurable: !0,
          writable: !0
        }) : e[t] = r, e
      }
  
      function ri() {
        var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : 60;
        return new Promise((function (t, r) {
          if (sr.hasAddon("record") && !rr.isSupported) return r(new ci("NoRecorder",
            "MediaRecorder API is not supported"));
          if ("function" != typeof window.getScreenDetails || Ft() || Zt()) o();
          else {
            var i = !1,
              n = setTimeout((() => {
                i = !0, r(new ci("NoWindowManagement", "No access to screen details"))
              }), 1e3 * e);
            window.getScreenDetails().then((() => {
              i || (clearTimeout(n), o())
            })).catch((() => {
              clearTimeout(n), r(new ci("NoWindowManagement", "No access to screen details"))
            }))
          }
  
          function o() {
            var e = 0,
              i = 0;
            setTimeout((function () {
              return hr.stop(), e <= 0 ? r(new ci("Unsupported", "Browser is not supported")) : i <=
                0 ? r(new ci("WrongSize", "This window is not maximized")) : void t()
            }), 5e3), hr.start((function (t) {
              e += t.supported ? 1 : -1, i += t.maximized ? 1 : -1
            }), {
              interval: 1,
              skip: 0
            })
          }
        }))
      }
  
      function ii(e) {
        var t = arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : 60;
        return new Promise((function (r, i) {
          var n = !1,
            o = setTimeout((() => {
              n = !0, i(new ci("NoVideo", "Request timeout"))
            }), 1e3 * t);
          Vt(ei({
            audio: !1,
            videoDeviceId: e
          }, l.get("webcam"))).then((e => {
            if (clearTimeout(o), n) return li(e);
            var t, a = 0;
            setTimeout((function () {
              var n;
              if ((Lr.stop(), li(e), t) && (t.stop(), null === (n = t.files) || void 0 ===
                  n || !n.length)) return i(new ci("NoRecorder",
                "Unable to record the camera"));
              if (a <= 0) return i(new ci("NoPicture", "No picture from the camera"));
              r()
            }), 1e4), sr.hasAddon("record") && (t = new rr({
              video: e,
              duration: 5
            })).start(), Lr.start(e, (function (e) {
              a += e ? 1 : -1
            }), {
              interval: 3
            })
          })).catch((e => {
            i(new ci("NoVideo", e.message))
          }))
        }))
      }
  
      function ni(e) {
        var t = arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : 60;
        return new Promise((function (r, i) {
          var n = !1,
            o = setTimeout((() => {
              n = !0, i(new ci("NoAudio", "Request timeout"))
            }), 1e3 * t);
          Vt(ei({
            video: !1,
            audioDeviceId: e
          }, l.get("webcam"))).then((e => {
            if (clearTimeout(o), n) return li(e);
            var t, a = 0;
            setTimeout((function () {
              var n;
              if ((Er.stop(), li(e), t) && (t.stop(), null === (n = t.files) || void 0 ===
                  n || !n.length)) return i(new ci("NoRecorder",
                "Unable to record the microphone"));
              if (a <= 0) return i(new ci("LowVolume", "Low microphone volume"));
              r()
            }), 1e4), sr.hasAddon("record") && (t = new rr({
              video: e,
              duration: 5
            })).start(), Er.start(e, (function (e) {
              a += e.muted ? -1 : 1
            }), {
              interval: 1,
              timeout: 3,
              skip: 0
            })
          })).catch((e => {
            i(new ci("NoAudio", e.message))
          }))
        }))
      }
  
      function oi() {
        var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : 60;
        return new Promise((function (t, r) {
          if (!sr.hasAddon("screen") || sr.hasAddon("mobile") && Zt()) return t();
          var i = !1,
            n = setTimeout((() => {
              i = !0, r(new ci("NoScreen", "Request timeout"))
            }), 1e3 * e);
          Vt(ei({
            source: "screen"
          }, l.get("screen"))).then((e => {
            if (clearTimeout(n), i) return li(e);
            var o = 0,
              a = 0;
            setTimeout((function () {
              return Kr.stop(), li(e), o <= 0 ? r(new ci("NoCapture",
                "No picture from the screen")) : a <= 0 ? r(new ci("Multiscreen",
                "Use more than one screen")) : void t()
            }), 1e4), Kr.start(e, (function (e) {
              o += e.captured ? 1 : -1, a += e.natural && e.single ? 1 : -1
            }), {
              interval: 3,
              skip: 0
            })
          })).catch((e => {
            r(new ci("NoScreen", e.message))
          }))
        }))
      }
  
      function ai() {
        var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : 5;
        return new Promise((function (t, r) {
          var i = 0;
          setTimeout((function () {
            if (Fr.stop(), i <= 0) return r(new ci("NoConnection", "WebSocket connection error"));
            t()
          }), 1e3 * e), Fr.start((function (e) {
            i += e.connected ? 1 : -1
          }), {
            interval: 1
          })
        }))
      }
  
      function si() {
        var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : 30;
        return new Promise(((t, r) => {
          (function (e) {
            var t = e.timeout,
              r = void 0 === t ? 30 : t,
              i = e.turnURI;
            class n {
              constructor(e) {
                var t = e || {},
                  r = t.iceServers,
                  i = t.toSendKb,
                  n = void 0 === i ? 1024 : i;
                this.sender = new RTCPeerConnection({
                  iceServers: r
                }), this.receiver = new RTCPeerConnection({
                  iceServers: r
                }), this.sender.onicecandidate = e => {
                  var t;
                  return "relay" === (null === (t = e.candidate) || void 0 === t ? void 0 : t
                    .type) && this.receiver.addIceCandidate(e.candidate)
                }, this.receiver.onicecandidate = e => {
                  var t;
                  return "relay" === (null === (t = e.candidate) || void 0 === t ? void 0 : t
                    .type) && this.sender.addIceCandidate(e.candidate)
                }, this.toSendKb = n, this.receivedBytes = 0
              }
              start() {
                return this._connect().then((() => (this._startSpeedTest(), this._endSpeedTest())))
              }
              close() {
                this.senderChannel.close(), this.receiverChannel.close(), this.sender.close(), this
                  .receiver.close()
              }
              _connect() {
                var e = this._openDataChannel();
                return this._createOffer().then((e => this._createAnswer(e))).then((() => e))
              }
              _startSpeedTest() {
                var e = "h".repeat(1024),
                  t = this.toSendKb;
                this.startTime = Date.now();
                for (var r = 0; r < t; r++) this._send(e)
              }
              _endSpeedTest() {
                return new Promise(((e, t) => {
                  this.resolveEndSpeedTest = e
                }))
              }
              _createOffer() {
                return this.sender.createOffer().then((e => this.sender.setLocalDescription(e).then((
                () => e))))
              }
              _createAnswer(e) {
                return this.receiver.setRemoteDescription(e).then((() => this.receiver
                  .createAnswer())).then((e => this.receiver.setLocalDescription(e).then((() => e))))
                  .then((e => this.sender.setRemoteDescription(e).then((() => e))))
              }
              _openDataChannel() {
                return new Promise(((e, t) => {
                  try {
                    this.senderChannel = this.sender.createDataChannel("webrtc-relay-check"),
                      this.senderChannel.onopen = t => e(), this.receiver.ondatachannel = e => {
                        this.receiverChannel = e.channel, this.receiverChannel.onmessage = e =>
                          this._messageReceived(e)
                      }
                  } catch (e) {
                    t(e)
                  }
                }))
              }
              _send(e) {
                this.senderChannel.send(e)
              }
              _messageReceived(e) {
                var t = Date.now();
                if (this.receivedBytes += e.data.length, this.receivedBytes >= 1024 * this.toSendKb) {
                  var r = t - this.startTime;
                  this.resolveEndSpeedTest({
                    sendedAt: this.startTime,
                    receivedAt: t,
                    time: r,
                    throughputBPS: this.receivedBytes / r * 8
                  })
                }
              }
            }
            return new Promise(((e, t) => {
              var o = setTimeout((() => {
                  var e = new Error("Connection timeout");
                  t(e)
                }), 1e3 * r),
                a = new n({
                  iceServers: er.getIceServers(i)
                });
              a.start().then((t => {
                clearTimeout(o), a.close(), e(t)
              })).catch((e => {
                clearTimeout(o), a.close(), t(e)
              }))
            }))
          })({
            timeout: e,
            turnURI: l.get("turnURI")
          }).then((e => {
            var i = e.throughputBPS,
              n = {
                audio: l.get("webcam.bitrate.audio"),
                webcam: l.get("webcam.bitrate.video"),
                screen: l.get("screen.bitrate.video")
              },
              o = n.audio,
              a = void 0 === o ? 16 : o,
              s = n.webcam,
              c = void 0 === s ? 64 : s,
              d = n.screen,
              u = void 0 === d ? 64 : d,
              p = Xr([a, c, u].map((e => parseInt(e))), 3);
            a = p[0], c = p[1], u = p[2], i < a + c + (sr.hasAddon("screen") ? u : 0) ? r(new ci(
              "RtcError", "Insufficient data transfer rate (".concat(i, " kbps)"))) : t()
          })).catch((e => {
            r(new ci("RtcError", e.message))
          }))
        }))
      }
      class ci extends Error {
        constructor() {
          var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : "Error";
          super(arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : ""), this.name = e
        }
      }
  
      function li(e) {
        e && "function" == typeof e.getTracks && e.getTracks().forEach((e => e.stop()))
      }
      var di = r(6062),
        ui = r.n(di),
        pi = r(4036),
        vi = r.n(pi),
        mi = r(6793),
        hi = r.n(mi),
        gi = r(7892),
        bi = r.n(gi),
        fi = r(1173),
        yi = r.n(fi),
        Mi = r(2464),
        ji = r.n(Mi),
        Pi = r(3500),
        Ti = {};
      Ti.styleTagTransform = ji(), Ti.setAttributes = bi(), Ti.insert = hi().bind(null, "head"), Ti.domAPI =
      vi(), Ti.insertStyleElement = yi();
      ui()(Pi.Z, Ti);
      const Li = Pi.Z && Pi.Z.locals ? Pi.Z.locals : void 0;
      var Ai, wi, ki = {
          en: JSON.parse(
            '{"signup":{"title":"Registration for the event","text":"Enter the parameters of the event you want to participate in. Usually, these parameters are provided by the event organizer.","username":"Your login","password":"Your password","template":"Event identifier","error":"Specified parameters are incorrect","button":{"ok":"OK"}},"wizard":{"title":{"rules":"Rules of the event","check":"Equipment check","profile":"Filling in the profile","face":"Taking a face photo","passport":"Taking a photo or uploading an ID","overview":"Recording a workplace overview","qrcode":"Mobile camera connection"},"button":{"next":"Next"},"page":"Step %{page} of %{total}"},"check":{"text":"Please wait while the system checks your computer and the network so that possible technical issues do not interfere with the exam.","empty":"Equipment check is not required.","stage":{"browser":"Browser check","camera":"Webcam check","microphone":"Microphone check","screen":"Screen check","network":"Network check","webrtc":"WebRTC check"},"button":{"retry":"Retry"},"error":{"Error":"Unknown error. Please try again.","Unsupported":"Browser or device is not supported. Use a different browser or another device.","WrongSize":"Your browser window is not in the fullscreen mode. Please switch it to the full screen mode.","NoRecorder":"MediaRecorder API is not supported or disabled. Please enable this API (Settings > Safari > Advanced > Experimental Features > MediaRecorder) or use a different browser.","NoWindowManagement":"Permission not granted to access multi-screen mode. Give access to the multi-screen window placement.","NoPicture":"No video from the camera. Try to close all other applications and disable your antivirus.","NoVideo":"Webcam is disabled or no webcam. Connect your webcam or enable the webcam access.","LowVolume":"Microphone has low volume or not working. Correct the volume or change your microphone.","NoAudio":"Microphone muted or disabled. Connect your microphone and enable the browser access to the microphone.","NoCapture":"No video from your screen. Enable the browser access to your screen.","Multiscreen":"You have not shared the entire screen. Enable the browser access to the entire screen and unplug any additional displays.","NoScreen":"Access to your screen is disabled or a part of your screen is blocked. Enable the browser access to the entire screen.","NoConnection":"WebSocket connection is blocked. Try to disable ad blocker like AdBlock or other similar browser extensions.","RtcError":"Unable to establish WebRTC connection. Try to turn off your firewall and antivirus, or connect to a different network."}},"profile":{"text":"Fill in or check your last name, first name and middle name (if available).","lastname":"Last name","firstname":"First name","middlename":"Middle name","error":{"unsaved":"An error occurred while saving data (%{code})"}},"face":{"text":"Take a photo with your face fitting into the oval frame on the screen. Make sure that there is enough light in the room. If the photo is not verified, please take a new photo.","button":{"retry":"Retry","take":"Take photo"},"msg":{"loading":"<p><b>Loading...</b></p>","nocamera":"<p><b>Problem with webcam detected :(</b></p><p>Please try the following:</p><ul><li>Connect your camera to the computer</li><li>Close all third-party applications that can use the camera.</li><li>Allow access to your camera in the browser</li></ul>","noface":"<p><b>Did not find you in the photo :(</b></p><p>Possible reasons:</p><ul><li>Your face is out of the frame</li><li>Poor lighting</li><li>The face is not clearly visible due to your hair or clothing.</li><li>The camera is on the side or too far away from you</li><li>The light source is behind you or on the side</li></ul><p>Try to take the photo again.</p>","unverified":"<p><b>Access denied :(</b></p><p>Your photo does not match with the photo in the member profile.</p>","done":"<p><b>Snapshot saved.</b></p><p>You can retake the picture if this photo does not suit you.</p>"}},"passport":{"text":{"photo":"Take a picture of your ID that clearly shows your photo and name.","scan":"Upload a scan of your ID that clearly shows your photo and name. The upload document format is JPEG or PNG.","both":"Take a picture or upload a scan of your ID that clearly shows your photo and name. The upload document format is JPEG or PNG."},"textExtra":{"photo":"Take a picture of another side of your ID.","scan":"Upload a scan of another side of your ID. The upload document format is JPEG or PNG.","both":"Take a picture or upload a scan of another sideof your ID. The upload document format is JPEG or PNG."},"button":{"retry":"Retry","take":"Take a picture","upload":"Upload","add":"+1 photo","reset":"Reset"},"msg":{"loading":"<p><b>Loading...</b></p>","ready":"<p><b>Please follow the requirements:</b></p><ul><li>File format JPEG or PNG</li><li>File size must not exceed 5 MB</li><li>Image resolution is not less than 1 Mpix</li><li>Horizontal file</li><li>The document must contain one photo of the face</li><li>Text and photo should be clearly recognisable</li></ul>","nocamera":"<p><b>Problem with webcam detected :(</b></p><p>Please try the following:</p><ul><li>Connect the camera to your computer</li><li>Close all third-party applications that can use the camera</li><li>Allow access to the camera in browser</li></ul>","nophoto":"<p><b>Document is not detected in the picture :(</b></p><p>Possible reasons:</p><ul><li>The document does not fit into the frame</li><li>The document is not horizontal</li><li>The face photo is not clear in the document</li><li>The text in the document is not recognisable</li><li>Name does not match `%{nickname}`</li></ul><p>Try to take the picture again.</p>","noscan":"<p><b>The document is not detected in the scan :(</b></p><p>Possible reasons:</p><ul><li>The file is not JPEG or PNG format</li><li>File size is more than 5 MB</li><li>Image resolution is less than 1 Mpix</li><li>Document is not horizontal</li><li>The photo or text in the document is not clear</li><li>Name does not match `%{nickname}`</li></ul><p>Try to upload a different file.</p>","unverified":"<p><b>Access denied :(</b></p><p>The document does not match with the document in the member profile.</p>","taken":"<p><b>The picture has been saved.</b></p><p>If unhappy with the picture, you can retake the picture.</p>","uploaded":"<p><b>The scanned document has been uploaded.</b></p><p>If unhappy with the image, you can upload the file again.</p>"}},"overview":{"text":"Record a short video showing your workspace (including a 360-degree scan of your surroundings) using your computer camera or smartphone camera. If using a smartphone, scan the QR code using your smartphone and then open the received link in Chrome browser on Android or Safari on iOS.","expires":"The link is valid until %{timeleft}","button":{"retry":"Retry","start":"Start recording","stop":"Stop recording","save":"Save","qrcode":"QR Code"},"msg":{"loading":"<p><b>Loading...</b></p>","nocamera":"<p><b>Problem with webcam detected :(</b></p><p>Please try the following:</p><ul><li>Connect your camera to the computer</li><li>Close all third-party applications that can use the camera.</li><li>Allow access to your camera in the browser</li></ul>","norecord":"<p><b>Problem with recording detected :(</b></p><p>Possible reasons:</p><ul><li>Your camera is not working properly</li><li>Your browser does not support the MediaRecorder API</li><li>There is a problem with the network</li></ul><p>Please try again or change your browser / computer.</p>","done":"<p><b>Video saved.</b></p><p>You can re-record if this video is not suitable for you.</p>"}},"qrcode":{"text":"Scan the QR code using your smartphone and then open the received link in Chrome browser on Android or Safari on iOS. Connect your smartphone to the charger and position the camera so that we can see your workplace, you and your computer.","expires":"The link is valid until %{timeleft}"},"ready":{"title":"Connection to the event","description":"Everything is ready, now you can start the event. If the event could not start, try again later or select another event.","nickname":"Full name","subject":"Event title","scheduled":"Scheduled time","deadline":"Expiration time","error":{"ERR_SESSION_NOT_FOUND":"You don\'t have any active session assigned to your profile. You can\'t proceed.","ERR_SEB_INVALID_SIGNATURE":"This event can only be carried out via the Safe Exam Browser, it\'s not possible to proceed via your current browser.","ERR_NO_PROCTORS_AVAILABLE":"There are no available proctors at the moment. Please try again later.","ERR_SESSION_TIME_NOT_COME":"The event hasn\'t started yet. Please, try again later.","ERR_SESSION_TIME_EXPIRED":"The event has been finished, it\'s not possible to continue.","ERR_INVALID_LICENSE":"Invalid license. You can\'t proceed until your vendor prolonged the license.","ERR_SERVICE_UNAVAILABLE":"The service is temporarily unavailable, please try again later."},"button":{"start":"Start"}},"chat":{"title":"Chat","inputPlaceholder":"Enter your message..."},"calculator":{"title":"Calculator"},"conference":{"guest":"Guest","microphone":"Microphone","camera":"Camera","screen":"Screen sharing","mute":"Sound on/off","single":"Display modes","maximize":"Block size"},"vision":{"qrcode":"Connect your mobile camera","events":{"b1":"Browser not supported","b2":"Focus switched to a different window","b3":"Full-screen mode disabled","c1":"Webcam disabled","c2":"Face invisible or not looking into the camera","c3":"Several faces in front of the camera","c4":"Face does not match the profile","c5":"Found similar profile","k1":"Atypical keyboard handwriting","m1":"Microphone muted or not working","m2":"There is conversation or background noise","n1":"No network connection","n2":"No connection to mobile camera","s1":"Screen activities not shared","s2":"Second display is used"},"button":{"ok":"OK"}},"duplicate":{"title":"Session is blocked","label":"Attention!","text":"This page was opened elsewhere, close this tab."},"finish":{"title":"Session complete","label":"Attention!","text":{"auto":"The session was terminated automatically.","proctor":"The session was terminated by the proctor."},"button":{"ok":"OK"}},"confirm":{"title":"Completion of the session","label":"Finish the session?","text":"Once completed, you will not be able to continue.","checkbox":"I understand and confirm the action","button":{"ok":"Yes","cancel":"No"}},"iframe":{"button":{"home":"Home page","finish":"Finish","chat":"Chat","calculator":"Calculator","qrcode":"QR Code"}}}'
            ),
          es: JSON.parse(
            '{"signup":{"title":"Registro para el evento","text":"Ingrese los parámetros del evento en el que desea participar. Por lo general, estos parámetros los proporciona el organizador del evento.","username":"Su nombre de usuario","password":"Tu contraseña","template":"Identificador de evento","error":"Los parámetros especificados son incorrectos","button":{"ok":"OK"}},"wizard":{"title":{"rules":"Reglas del evento","check":"Comprobación de equipos","profile":"Rellenando el perfil","face":"Tomando una foto de la cara","passport":"Tomar una foto o cargar una identificación","overview":"Grabación de una descripción general del lugar de trabajo","qrcode":"Conexión de cámara móvil"},"button":{"next":"Próximo"},"page":"Paso %{page} de %{total}"},"check":{"text":"Espere mientras el sistema revisa su computadora y la red para que posibles problemas técnicos no interfieran con el examen.","empty":"No se requiere verificación de equipo.","stage":{"browser":"Comprobación del navegador","camera":"Comprobación de cámara web","microphone":"Comprobación de micrófono","screen":"Comprobación de pantalla","network":"Comprobación de red","webrtc":"Comprobación WebRTC"},"button":{"retry":"Rever"},"error":{"Error":"Error desconocido. Vuelve a intentarlo.","Unsupported":"El navegador o el dispositivo no es compatible. Use un navegador diferente u otro dispositivo.","WrongSize":"La ventana de su navegador no está en el modo de pantalla completa. Cámbiela al modo de pantalla completa.","NoRecorder":"La API de MediaRecorder no es compatible o está deshabilitada. Habilite esta API (Configuración > Safari > Avanzado > Funciones experimentales > MediaRecorder) o use un navegador diferente.","NoWindowManagement":"Permiso no otorgado para acceder al modo multipantalla. Dar acceso a la ubicación de la ventana multipantalla.","NoPicture":"No hay video de la cámara. Intente cerrar todas las demás aplicaciones y desactive su antivirus.","NoVideo":"La cámara web está deshabilitada o no hay cámara web. Conecte su cámara web o habilite el acceso a la cámara web.","LowVolume":"El micrófono tiene un volumen bajo o no funciona. Corrija el volumen o cambie el micrófono.","NoAudio":"Micrófono silenciado o deshabilitado. Conecte su micrófono y habilite el acceso del navegador al micrófono.","NoCapture":"No hay video de su pantalla. Habilite el acceso del navegador a su pantalla.","Multiscreen":"No ha compartido toda la pantalla. Habilite el acceso del navegador a toda la pantalla y desconecte cualquier pantalla adicional.","NoScreen":"El acceso a su pantalla está deshabilitado o una parte de su pantalla está bloqueada. Habilite el acceso del navegador a toda la pantalla.","NoConnection":"La conexión de WebSocket está bloqueada. Intente deshabilitar el bloqueador de anuncios como AdBlock u otras extensiones de navegador similares.","RtcError":"No se puede establecer la conexión WebRTC. Intente apagar su firewall y antivirus, o conéctese a una red diferente."}},"profile":{"text":"Complete o marque su apellido, nombre y segundo nombre (si está disponible).","lastname":"Apellido","firstname":"Nombre","middlename":"Segundo nombre","error":{"unsaved":"Ocurrió un error al guardar los datos (%{code})"}},"face":{"text":"Haz una foto con tu cara encajando en el marco ovalado de la pantalla. Asegúrese de que haya suficiente luz en la habitación. Si la foto no está verificada, tome una nueva foto.","button":{"retry":"Rever","take":"Tomar foto"},"msg":{"loading":"<p><b>Cargando...</b></p>","nocamera":"<p><b>Se detectó un problema con la cámara web :(</b></p><p>Intente lo siguiente:</p><ul><li>Conecte su cámara a la computadora</li><li>Cierre todas las aplicaciones de terceros que puedan usar la cámara.</li><li>Permita el acceso a su cámara en el navegador</li></ul>","noface":"<p><b>No te encontré en la foto :(</b></p><p>Posibles razones:</p><ul><li>Tu cara está fuera del marco</li><li>Pobre iluminación</li><li>La cara no es claramente visible debido a su cabello o ropa.</li><li>La cámara está a un lado o demasiado lejos de usted</li><li>La fuente de luz está detrás de ti o al costado</li></ul><p>Intenta tomar la foto nuevamente.</p>","unverified":"<p><b>Acceso denegado :(</b></p><p>Tu foto no coincide con la foto del perfil del miembro.</p>","done":"<p><b>Instantánea guardada.</b></p><p>Puede volver a tomar la foto si esta foto no le conviene.</p>"}},"passport":{"text":{"photo":"Tome una foto de su identificación que muestre claramente su foto y nombre.","scan":"Cargue un escaneo de su identificación que muestre claramente su foto y nombre. El formato del documento de carga es JPEG o PNG.","both":"Tome una foto o cargue un escaneo de su identificación que muestre claramente su foto y nombre. El formato del documento de carga es JPEG o PNG."},"textExtra":{"photo":"Toma una foto del otro lado de tu identificación.","scan":"Cargue un escaneo de otro lado de su identificación. El formato del documento de carga es JPEG o PNG.","both":"Tome una foto o cargue un escaneo de otro lado de su identificación. El formato del documento de carga es JPEG o PNG."},"button":{"retry":"Rever","take":"Toma una foto","upload":"Subir","add":"+1 foto","reset":"Reiniciar"},"msg":{"loading":"<p><b>Cargando...</b></p>","ready":"<p><b>Siga los requisitos:</b></p><ul><li>Formato de archivo JPEG o PNG</li><li>El tamaño del archivo no debe exceder los 5 MB</li><li>La resolución de la imagen no debe ser inferior a 1 Mpix</li><li>Archivo horizontal</li><li>El documento debe contener una foto de la cara</li><li>El texto y la foto deben ser claramente reconocibles</li></ul>","nocamera":"<p><b>Se detectó un problema con la cámara web :(</b></p><p>Intente lo siguiente:</p><ul><li>Conecte la cámara a su computadora</li><li>Cierre todas las aplicaciones de terceros que puedan usar la cámara</li><li>Permita el acceso a la cámara en el navegador</li></ul>","nophoto":"<p><b>No se detecta el documento en la imagen :(</b></p><p>Posibles razones:</p><ul><li>El documento no cabe en el marco</li><li>El documento no es horizontal</li><li>La foto de la cara no está clara en el documento</li><li>El texto del documento no es reconocible</li><li>El nombre sí no coincide con `%{nickname}`</li></ul><p>Intenta tomar la foto nuevamente.</p>","noscan":"<p><b>El documento no se detecta en el escaneo :(</b></p><p>Posibles razones:</p><ul><li>El archivo no tiene formato JPEG o PNG</li><li>El tamaño del archivo es superior a 5 MB</li><li>La resolución de la imagen es inferior a 1 megapíxel</li><li>El documento no está en posición horizontal</li><li>La foto o el texto en el documento no está claro</li><li>El nombre no coincide con `%{nickname}`</li></ul><p>Intente cargar un archivo diferente.</p>","unverified":"<p><b>Acceso denegado :(</b></p><p>El documento no coincide con el documento en el perfil del miembro.</p>","taken":"<p><b>La imagen se ha guardado.</b></p><p>Si no está satisfecho con la imagen, puede volver a tomarla.</p>","uploaded":"<p><b>El documento escaneado ha sido cargado.</b></p><p>Si no está satisfecho con la imagen, puede cargar el archivo nuevamente.</p>"}},"overview":{"text":"Grabe un video corto que muestre su espacio de trabajo (incluido un escaneo de 360 grados de su entorno) usando la cámara de su computadora o la cámara de su teléfono inteligente. Si usa un teléfono inteligente, escanee el código QR usando su teléfono inteligente y luego abra el enlace recibido en el navegador Chrome en Android o Safari en iOS.","expires":"El enlace es válido hasta %{timeleft}","button":{"retry":"Rever","start":"Empezar a grabar","stop":"Para de grabar","save":"Ahorrar","qrcode":"Código QR"},"msg":{"loading":"<p><b>Cargando...</b></p>","nocamera":"<p><b>Se detectó un problema con la cámara web :(</b></p><p>Intente lo siguiente:</p><ul><li>Conecte su cámara a la computadora</li><li>Cierre todas las aplicaciones de terceros que puedan usar la cámara.</li><li>Permita el acceso a su cámara en el navegador</li></ul>","norecord":"<p><b>Problema con la grabación detectado :(</b></p><p>Posibles razones:</p><ul><li>Tu cámara no funciona correctamente</li><li>Tu navegador no es compatible con la API de MediaRecorder</li><li>Hay un problema con la red</li></ul><p>Por favor, inténtalo de nuevo o cambia tu navegador/ordenador.</p>","done":"<p><b>Video guardado.</b></p><p>Puede volver a grabar si este video no es adecuado para usted.</p>"}},"qrcode":{"text":"Escanee el código QR con su teléfono inteligente y luego abra el enlace recibido en el navegador Chrome en Android o Safari en iOS. Conecte su teléfono inteligente al cargador y coloque la cámara para que podamos ver su lugar de trabajo, usted y su computadora.","expires":"El enlace es válido hasta%{timeleft}"},"ready":{"title":"Conexión al evento","description":"Todo está listo, ahora puede iniciar el evento. Si el evento no pudo iniciar, vuelva a intentarlo más tarde o seleccione otro evento.","nickname":"Nombre completo","subject":"Título del evento","scheduled":"Hora programada","deadline":"Tiempo de expiración","error":{"ERR_SESSION_NOT_FOUND":"No tienes ninguna sesión activa asignada a tu perfil. No puedes continuar.","ERR_SEB_INVALID_SIGNATURE":"Este evento solo se puede llevar a cabo a través de Safe Exam Browser, no es posible continuar a través de su navegador actual.","ERR_NO_PROCTORS_AVAILABLE":"No hay supervisores disponibles en este momento. Por favor, inténtelo de nuevo más tarde.","ERR_SESSION_TIME_NOT_COME":"El evento aún no ha comenzado. Por favor, inténtelo de nuevo más tarde.","ERR_SESSION_TIME_EXPIRED":"El evento ha finalizado, no es posible continuar.","ERR_INVALID_LICENSE":"Licencia invalida. No puede continuar hasta que su proveedor prolongue la licencia.","ERR_SERVICE_UNAVAILABLE":"El servicio no está disponible temporalmente, inténtelo de nuevo más tarde."},"button":{"start":"Comenzar"}},"chat":{"title":"Charlar","inputPlaceholder":"Ingrese su mensaje..."},"calculator":{"title":"Calculadora"},"conference":{"guest":"Invitado","microphone":"Micrófono","camera":"Cámara","screen":"Compartir pantalla","mute":"Sonido activado/desactivado","single":"Modos de visualización","maximize":"Tamaño de bloque"},"vision":{"qrcode":"Conecta la cámara de tu móvil","events":{"b1":"Navegador no compatible","b2":"Enfoque cambiado a una ventana diferente","b3":"Modo de pantalla completa deshabilitado","c1":"Cámara web deshabilitada","c2":"Rostro invisible o que no mira a la cámara","c3":"Varios rostros frente a la cámara","c4":"La cara no coincide con el perfil","c5":"Encontrado un perfil similar","k1":"Escritura de teclado atípica","m1":"Micrófono silenciado o no funciona","m2":"Hay conversación o ruido de fondo","n1":"No hay conexion de red","n2":"Sin conexión con la cámara del móvil","s1":"Actividades de pantalla no compartidas","s2":"Se utiliza la segunda pantalla"},"button":{"ok":"OK"}},"duplicate":{"title":"La sesión está bloqueada","label":"¡Atención!","text":"Esta página se abrió en otro lugar, cierre esta pestaña."},"finish":{"title":"Sesión completa","label":"¡Atención!","text":{"auto":"La sesión se terminó automáticamente.","proctor":"La sesión fue terminada por el supervisor."},"button":{"ok":"OK"}},"confirm":{"title":"Finalización de la sesión","label":"Terminar la sesión?","text":"Una vez completado, no podrá continuar.","checkbox":"Entiendo y confirmo la acción","button":{"ok":"Sí","cancel":"No"}},"iframe":{"button":{"home":"Página de inicio","finish":"Finalizar","chat":"Charlar","calculator":"Calculadora","qrcode":"Código QR"}}}'
            ),
          fi: JSON.parse(
            '{"signup":{"title":"Ilmoittautuminen tapahtumaan","text":"Anna sen tapahtuman parametrit, joihin haluat osallistua. Yleensä nämä parametrit tarjoaa tapahtuman järjestäjä.","username":"Kirjaudu sisään","password":"Salasanasi","template":"Tapahtuman tunniste","error":"Määritetyt parametrit ovat virheellisiä","button":{"ok":"KUNNOSSA"}},"wizard":{"title":{"rules":"Tapahtuman säännöt","check":"Laitteiden tarkistus","profile":"Profiilin täyttäminen","face":"Kasvokuvan ottaminen","passport":"Henkilöllisyystodistuksen lataaminen","overview":"Työpaikan yleiskatsauksen tallentaminen","qrcode":"Mobiilikamerayhteys"},"button":{"next":"Seuraava"},"page":"Vaihe %{page}/%{total}"},"check":{"text":"Odota, kun järjestelmä tarkistaa tietokoneen ja verkon niin, että mahdolliset tekniset ongelmat eivät häiritse tenttiä.","empty":"Laitteiden tarkistusta ei tarvita.","stage":{"browser":"Selaimen tarkistus","camera":"Web-kameran tarkistus","microphone":"Mikrofonin tarkistus","screen":"Näytön tarkistus","network":"Verkon tarkistus","webrtc":"WebRTC tarkistus"},"button":{"retry":"Yritä uudelleen"},"error":{"Error":"Tuntematon virhe. Yritä uudelleen.","Unsupported":"Selainta tai laitetta ei tueta. Käytä toista selainta tai toista laitetta.","WrongSize":"Selainikkunasi ei ole koko näytön tilassa. Vaihda se koko näytön tilaan.","NoRecorder":"MediaRecorder API:ta ei tueta tai sitä ei ole poistettu käytöstä. Ota tämä API käyttöön (Asetukset > Safari > Lisäasetukset > Kokeelliset ominaisuudet > MediaRecorder) tai käytä toista selainta.","NoWindowManagement":"Usean näytön tilaan pääsyä ei ole myönnetty. Anna pääsy usean näytön ikkunan sijoitteluun.","NoPicture":"Ei videota kamerasta. Yritä sulkea kaikki muut sovellukset ja poistaa virustorjunta käytöstä.","NoVideo":" Web-kamera on poistettu käytöstä tai web-kameraa ei ole. Yhdistä web-kamerasi tai salli web-kameran käyttö.","LowVolume":"Mikrofoni on pieni tai ei toimi. Korjaa äänenvoimakkuus tai muuta mikrofoni.","NoAudio":"Mikrofoni mykistetty tai poistettu käytöstä. Liitä mikrofoni ja salli selaimen pääsy mikrofoniin.","NoCapture":"Ei videota näytöltäsi. Salli selaimen pääsy näytöllesi.","Multiscreen":"Et ole jakanut koko näyttöä. Salli selaimen pääsy koko näyttöön ja irrota mahdolliset lisänäytöt.","NoScreen":"Pääsy näytöllesi on estetty tai osa näytöstä on estetty. Salli selaimen pääsy koko näyttöön.","NoConnection":"WebSocket-yhteys on estetty. Yritä poistaa käytöstä mainosten esto, kuten AdBlock tai muut vastaavat selainlaajennukset.","RtcError":" WebRTC-yhteyttä ei voida muodostaa. Yritä ottaa pois päältä palomuuri ja virustorjunta tai muodosta yhteys toiseen verkkoon."}},"profile":{"text":"Täytä tai tarkista sukunimesi, etunimesi ja toinen nimesi (jos saatavilla).","lastname":"Sukunimi","firstname":"Etunimi","middlename":"Toinen nimi","error":{"unsaved":"Tietoa tallennettaessa tapahtui virhe (%{code})"}},"face":{"text":"Ota kuva niin, että kasvosi sopivat näytön soikeaan kehykseen. Varmista, että huoneessa on riittävästi valoa. Jos kuvaa ei ole vahvistettu, ota uusi kuva.","button":{"retry":"Yrittää uudelleen","take":"Ota kuva"},"msg":{"loading":"<p><b>Ladataan...</b></p>","nocamera":"<p><b>Ongelma web-kamerassa havaittu :(</b></p><p>Kokeile seuraavaa:</p><ul><li>Yhdistä kamera tietokoneeseen</li><li>Sulje kaikki kolmannen osapuolen sovellukset, jotka voivat käyttää kameraa.</li><li>Salli pääsy kameraan selaimessa</li></ul>","noface":"<p><b>Ei löytänyt sinua kuvassa: (</b></p><p>Mahdolliset syyt:</p><ul><li>Kasvosi on poissa kehyksestä</li><li>Huono valaistus</li></li>Kasvot eivät ole selvästi näkyvissä hiusten tai vaatteiden vuoksi.</li><li>Kamera on sivussa tai liian kaukana sinusta</li><li>Valonlähde on takana tai sivulla</li></ul><p>Yritä ottaa valokuva uudelleen.</p>","unverified":"<p><b>Pääsy kielletty :(</b></p><p>Kuvasi ei täsmää jäsenprofiilissa olevan kuvan kanssa.</p>","done":"<p><b>Kuva tallennettu.</b></p><p>Voit ottaa kuvan uudelleen, jos et ole tyytyväinen tähän kuvaan.</p>"}},"passport":{"text":{"photo":"Ota kuva henkilöllisyystodistuksestasi, jossa näkyy selvästi kuvasi ja nimesi.","scan":"Lataa skannattu henkilöllisyystodistus, jossa näkyy selvästi kuvasi ja nimesi. Ladattavan asiakirjan muoto on JPEG tai PNG.","both":"Ota kuva tai lataa skannattu henkilöllisyystodistus, jossa näkyy selvästi kuvasi ja nimesi. Ladattavan asiakirjan muoto on JPEG tai PNG."},"textExtra":{"photo":"Ota valokuva henkilöllisyystodistuksen toisesta sivusta.","scan":"Lataa skannaus henkilöllisyystodistuksen toisesta sivusta. Ladattavan asiakirjan muoto on JPEG tai PNG.","both":"Ota valokuva tai lataa skannaus henkilöllisyystodistuksesi toisesta sivusta. Ladattavan asiakirjan muoto on JPEG tai PNG."},"button":{"retry":"Yrittää uudelleen","take":"Ota kuva","upload":"Lataa ","add":"Lataa lisää kuvia","reset":"Nollata"},"msg":{"loading":"<p><b>Ladataan...</b></p>","ready":"<p><b>Noudata vaatimuksia:</b></p><ul><li>Tiedostomuoto JPEG tai PNG</li><li>Tiedostokoko ei saa ylittää 5 Mt</li><li>Kuvan resoluutio on vähintään 1 megapikseliä</li><li>Vaakasuuntainen tiedosto</li><li>Asiakirjassa on oltava yksi valokuva</li><li>Tekstin ja valokuvan tulee olla selvästi tunnistettavissa</li></ul>","nocamera":"<p><b>Ongelma web-kamerassa havaittu :(</b></p><p>Kokeile seuraavaa:</p><ul><li>Yhdistä kamera tietokoneeseesi</li><li>Sulje kaikki kolmannen osapuolen sovellukset, jotka voivat käyttää kameraa</li><li>Salli pääsy kameraan selaimessa</li></ul>","nophoto":"<p><b>Asiakirjaa ei löydy kuvasta :(</b></p><p>Mahdollisia syitä:</p><ul><li>Asiakirja ei mahdu kokonaan kehykseen</li><li>Asiakirja ei ole vaakasuora</li><li>Kuva ei ole selkeä asiakirjassa</li><li>Dokumentissa oleva teksti ei ole tunnistettavissa</li><li>Nimi ei täsmää `%{nickname}`</li></ul><p>Yritä ottaa kuva uudelleen.</p>","noscan":"<p><b>Asiakirjaa ei havaittu skannauksessa :(</b></p><p>Mahdollisia syitä:</p><ul><li>Tiedosto ei ole JPEG- tai PNG-muotoinen</p></li><li>Tiedoston koko on yli 5 Mt</li><li>Kuvan resoluutio on alle 1 megapikseliä</li><li>Asiakirja ei ole vaakasuora</li><li>Asiakirjan valokuva tai teksti ei ole selkeä</li><li>Nimi ei täsmää `%{nickname}`</li></ul><p>Yritä ladata toinen tiedosto.</p>","unverified":"<p><b>Pääsy evätty :(</b></p><p> Asiakirja ei vastaa jäsenprofiilissa olevaa asiakirjaa.</p>","taken":"<p><b>Kuva tallennettu.</b></p><p>Jos et ole tyytyväinen kuvaan, voit ottaa kuvan uudelleen.</p>","uploaded":"<p><b>Skannattu asiakirja on ladattu.</b></p><p>Jos et ole tyytyväinen kuvaan, voit ladata tiedoston uudelleen.</p>"}},"overview":{"text":"Tallenna lyhyt video työtilastasi tietokoneen kameralla tai älypuhelimen kameralla. Jos käytät älypuhelinta, skannaa QR-koodi älypuhelimellasi ja avaa sitten saatu linkki Chrome-selaimessa Androidissa tai Safarissa iOS:ssä.","expires":"Linkki on voimassa %{timeleft}","button":{"retry":"Yrittää uudelleen","start":"Aloita nauhottaminen","stop":"Lopeta tallennus","save":"Tallentaa","qrcode":"QR koodi"},"msg":{"loading":"<p><b>Ladataan...</b></p>","nocamera":"<p><b>Ongelma web-kamerassa havaittu :(</b></p><p>Kokeile seuraavaa:</p><ul><li>Yhdistä kamera tietokoneeseen</li><li>Sulje kaikki kolmannen osapuolen sovellukset, jotka voivat käyttää kameraa.</li><li>Salli pääsy kameraan selaimessa</li></ul>","norecord":"<p><b>Ongelma tallennuksen kanssa havaittu :(</b></p><p>Mahdollisia syitä:</p><ul><li>Kamerasi ei toimi kunnolla</li><li>Selaimesi ei tue MediaRecorder API:ta</li><li>Verkossa on ongelma</li></ul><p>Yritä uudelleen tai vaihda selaimesi / tietokoneesi.</p>","done":"<p><b>Video tallennettu.</b></p><p>Voit tallentaa uudelleen, jos tämä video ei sovi sinulle.</p>"}},"qrcode":{"text":"Skannaa QR-koodi älypuhelimellasi ja avaa saatu linkki Chrome-selaimessa Androidissa tai Safarissa iOS:ssä. Liitä älypuhelimesi laturiin ja aseta kamera niin, että näemme työympäristösi, sinut ja tietokoneesi.","expires":"Linkki on voimassa %{timeleft}"},"ready":{"title":"Yhteys tapahtumaan","description":"Kaikki on valmista, voit aloittaa tapahtuman. Jos tapahtuman aloittaminen ei onnistu, yritä myöhemmin uudelleen tai valitse toinen tapahtuma.","nickname":"Nimi","subject":"Tapahtuman nimi","scheduled":"Ajastettu aika","deadline":"Päättymisaika","error":{"ERR_SESSION_NOT_FOUND":"Profiilillesi ei ole määritetty aktiivista istuntoa. Et voi jatkaa.","ERR_SEB_INVALID_SIGNATURE":"Tämä tapahtuma voidaan suorittaa vain turvallisen selaimen kautta, eteneminen ei ole mahdollista nykyisellä selaimellasi.","ERR_NO_PROCTORS_AVAILABLE":"Tällä hetkellä ei ole vapaita valvojia. Yritä uudelleen myöhemmin.","ERR_SESSION_TIME_NOT_COME":"Tapahtuma ei ole vielä alkanut. Yritä uudelleen myöhemmin.","ERR_SESSION_TIME_EXPIRED":"Tapahtuma on päättynyt, ei ole mahdollista jatkaa.","ERR_INVALID_LICENSE":"Virheellinen lisenssi. Et voi jatkaa ennen kuin myyjä on pidentänyt lisenssiä.","ERR_SERVICE_UNAVAILABLE":"Palvelu ei ole tilapäisesti käytettävissä, yritä myöhemmin uudelleen."},"button":{"start":"Aloita"}},"chat":{"title":"Chat","inputPlaceholder":"Syötä viestisi..."},"calculator":{"title":"Laskin"},"conference":{"guest":"Vieras","microphone":"Mikrofoni","camera":"Kamera","screen":"Näytön jakaminen","mute":"Ääni päälle/pois päältä","single":"Näytön tila","maximize":"Kuvakkeen koko"},"vision":{"qrcode":"Liitä mobiilikamera","events":{"b1":"Selainta ei tueta","b2":"Tarkennus siirtyi toiseen ikkunaan","b3":"Koko näytön tila ei ole käytössä","c1":"Web-kamera on poistettu käytöstä","c2":"Kasvot näkymättömät tai eivät katso kameraan","c3":"Useita kasvoja kameran edessä","c4":"Kasvot eivät vastaa profiilia","c5":"Löytyi samankaltainen profiili","k1":"Epätyypillinen näppäimistön käsiala","m1":"Mikrofoni mykistetty tai ei toimi","m2":"Taustalla on keskustelua tai melua","n1":"Ei verkkoyhteyttä","n2":"Ei yhteyttä mobiilikameraan","s1":"Näyttötoimintaa ei ole jaettu","s2":"Toista näyttöä käytetään"},"button":{"ok":"Ok"}},"duplicate":{"title":"Istunto on estetty","label":"Huomio!","text":"Tämä sivu avattiin muualla, sulje tämä välilehti."},"finish":{"title":"Istunto valmis","label":"Huomio!","text":{"auto":"Istunto lopetettiin automaattisesti.","proctor":"Valvoja lopetti istunnon."},"button":{"ok":"Ok"}},"confirm":{"title":"Istunnon päättäminen","label":"Lopeta istunto?","text":"Kun päätetty, et voi enää jatkaa.","checkbox":"Ymmärrän ja vahvistan toiminnon","button":{"ok":"Kyllä","cancel":"Ei"}},"iframe":{"button":{"home":"Kotisivu","finish":"Lopeta","chat":"Chat","calculator":"Laskin","qrcode":"QR koodi"}}}'
            ),
          fr: JSON.parse(
            '{"signup":{"title":"Inscription à l\'événement","text":"Entrez les paramètres de l\'événement auquel vous souhaitez participer. Ces paramètres sont généralement fournis par l\'organisateur de l\'événement.","username":"Votre identifiant","password":"Votre mot de passe","template":"Identifiant d\'événement","error":"Les paramètres spécifiés sont incorrects","button":{"ok":"OK"}},"wizard":{"title":{"rules":"Règles de l\'événement","check":"Vérification de l\'équipement","profile":"Remplir le profil","face":"Prendre une photo de visage","passport":"Prendre une photo de votre pièce d\'identité","overview":"Enregistrement d\'un aperçu du lieu de travail","qrcode":"Connexion à une caméra mobile"},"button":{"next":"Suivant"},"page":"Étape %{page} de %{total}"},"check":{"text":"Veuillez patienter pendant que le système vérifie votre équipement et votre connexion afin d\'éviter d\'éventuels problèmes techniques","empty":"La vérification n\'est pas nécessaire.","stage":{"browser":"Vérification du navigateur","camera":"Vérification de la camera","microphone":"Vérification du microphone","screen":"Vérification de l\'écran","network":"Vérification du réseau","webrtc":"Vérification WebRTC"},"button":{"retry":"Réessayer"},"error":{"Error":"Erreur inconnue. Veuillez réessayer.","Unsupported":"Votre navigateur n\'est pas supporté. Mettez votre navigateur à jour ou utilisez un autre navigateur.","WrongSize":"La fenêtre du navigateur n\'est pas en mode plein écran. Veuillez passer en mode plein écran.","NoRecorder":"L\'API de MediaRecorder n\'est pas prise en charge ou désactivée. Veuillez activer cette API ou utiliser un autre navigateur.","NoWindowManagement":"Autorisation non accordée pour accéder au mode multi-écrans. Donner accès au placement de la fenêtre multi-écrans.","NoPicture":"Pas de vidéo de la caméra. Essayez de fermer toutes les autres applications et de désactiver l\'antivirus.","NoVideo":"Webcam désactivée ou pas de webcam. Connectez votre webcam ou activez l\'accès à la webcam.","LowVolume":"Le microphone a un faible volume ou ne fonctionne pas. Corrigez le volume ou changez de microphone.","NoAudio":"Le microphone est coupé ou désactivé. Connectez le microphone et activez l\'accès au microphone par le navigateur.","NoCapture":"Pas de vidéo à l\'écran. Activer l\'accès à la caméra par le navigateur.","Multiscreen":"Vous n\'avez pas partagé l\'intégralité de l\'écran. Activez l\'accès du navigateur à l\'ensemble de l\'écran et débranchez tous les écrans supplémentaires.","NoScreen":"L\'accès à l\'écran est désactivé ou une partie de l\'écran est bloquée. Activez l\'accès au navigateur pour tout l\'écran.","NoConnection":"La connexion WebSocket est bloquée. Essayez de désactiver le bloqueur de publicité comme AdBlock ou des extensions de navigateur similaires.","RtcError":"Impossible d\'établir la connexion WebRTC. Essayez de désactiver votre pare-feu et votre antivirus, ou connectez-vous à un autre réseau."}},"profile":{"text":"Remplissez ou vérifiez votre nom, prénom et deuxième prénom (si disponible).","lastname":"Nom de famille","firstname":"Prénom","middlename":"Deuxième nom","error":{"unsaved":"Une erreur s\'est produite lors de l\'enregistrement des données (%{code})"}},"face":{"text":"Prenez une photo avec votre visage s\'inscrivant dans le cadre ovale à l\'écran. Assurez-vous qu\'il y a suffisamment de lumière dans la pièce. Si la photo n\'est pas vérifiée, veuillez prendre une nouvelle photo.","button":{"retry":"Réessayer","take":"Prenez une photo"},"msg":{"loading":"<p><b>Chargement...</b></p>","nocamera":"<p><b>Un problème de webcam détecté :(</b></p><p>Essayez ça :</p><ul><li>Connectez l\'appareil photo à l\'ordinateur</li><li>Fermez toutes les applications tierces qui peuvent utiliser l\'appareil photo.</li><li>Autoriser l\'accès à la caméra dans le navigateur</li></ul>","noface":"<p><b>Impossible de vous trouver sur la photo :(</b></p><p>Les raisons possibles :</p><ul><li>Visage hors cadre</li><li>Faible éclairage</li><li>Le visage n\'est pas clairement visible à cause des cheveux ou des vêtements.</li><li>La caméra est sur le côté ou trop éloignée de vous</li><li>La source de lumière est derrière vous ou sur le côté</li></ul><p>Essayez à nouveau de prendre une photo.</p>","unverified":"<p><b>Accès refusé :(</b></p><p>Votre photo ne correspond pas à la photo du profil du membre.</p>","done":"<p><b>Image sauvegardée.</b></p><p>Vous pouvez reprendre la photo si elle ne vous convient pas.</p>"}},"passport":{"text":{"photo":"Prenez une photo de votre pièce d\'identité qui montre clairement votre photo et votre nom.","scan":"Téléchargez un scan de votre pièce d\'identité qui montre clairement votre photo et votre nom. Le format du document de téléchargement est JPEG ou PNG.","both":"Prenez une photo ou téléchargez un scan de votre pièce d\'identité qui montre clairement votre photo et votre nom. Le format du document de téléchargement est JPEG ou PNG."},"textExtra":{"photo":"Prenez une photo de l\'autre page de votre document d\'identité.","scan":"Téléchargez un scan d\'une autre page de votre document d\'identité. Le format du document à télécharger est JPEG ou PNG.","both":"Prenez une photo ou téléchargez un scan d\'une autre page de votre document d\'identité. Le format du document à télécharger est JPEG ou PNG."},"button":{"retry":"Réessayer","take":"Prenez une photo","upload":"Télécharger","add":"+1 photo","reset":"Réinitialiser"},"msg":{"loading":"<p><b>Chargement...</b></p>","ready":"<p><b>Veuillez suivre les exigences:</b></p><ul><li>Format de fichier JPEG ou PNG</li><li>La taille du fichier ne doit pas dépasser 5 MB</li><li>La résolution d\'image n\'est pas inférieure à 1 Mpix</li><li>Fichier horizontal</li><li>Le document doit contenir une photo</li><li>Le texte et la photo doivent être clairement reconnaissables</li></ul>","nocamera":"<p><b>Problème de webcam détecté :(</b></p><p>S\'il vous plaît essayez ce qui suit:</p><ul><li>Connectez l\'appareil photo à votre ordinateur</li><li>Fermez toutes les applications tierces pouvant utiliser la caméra</li><li>Autoriser l\'accès à la caméra dans le navigateur</li></ul>","nophoto":"<p><b>Le document n\'est pas détecté dans l\'image :(</b></p><p>Raisons possibles:</p><ul><li>Le document ne rentre pas complètement dans le cadre</li><li>Le document n\'est pas horizontal</li><li>La photo n\'est pas claire dans le document</li><li>Le texte du document n\'est pas reconnaissable</li><li>Le nom ne correspond pas `%{nickname}`</li></ul><p>Essayez de reprendre la photo.</p>","noscan":"<p><b>Le document n\'est pas détecté lors de la numérisation :(</b></p><p>Raisons possibles:</p><ul><li>Le fichier n\'est pas au format JPEG ou PNG</li><li>La taille du fichier est supérieure à 5 MB</li><li>La résolution d\'image est inférieure à 1 Mpix</li><li>Le document n\'est pas horizontal</li><li>La photo ou le texte du document n\'est pas clair</li><li>Le nom ne correspond pas `%{nickname}`</li></ul><p>Essayez de télécharger un autre fichier.</p>","unverified":"<p><b>Accès refusé :(</b></p><p> Le document ne correspond pas au document dans le profil du membre.</p>","taken":"<p><b>L\'image a été enregistrée.</b></p><p>Si vous n\'êtes pas satisfait de la photo, vous pouvez la reprendre.</p>","uploaded":"<p><b>Le document numérisé a été téléchargé.</b></p><p>Si vous n\'êtes pas satisfait de l\'image, vous pouvez télécharger à nouveau le fichier.</p>"}},"overview":{"text":"Enregistrez une courte vidéo montrant votre espace de travail à l\'aide de la caméra de votre ordinateur ou de votre smartphone (y compris une analyse à 360 degrés de votre environnement). Si vous utilisez un smartphone, scannez le code QR à l\'aide de votre smartphone, puis ouvrez le lien reçu dans le navigateur Chrome sur Android ou Safari sur iOS.","expires":"Le lien est valide jusqu\'à %{timeleft}","button":{"retry":"Réessayer","start":"Commencer l\'enregistrement","stop":"Arrête d\'enregistrer","save":"Sauvegarder","qrcode":"QR Code"},"msg":{"loading":"<p><b>Chargement...</b></p>","nocamera":"<p><b>Problème de webcam détecté :(</b></p><p>S\'il vous plaît essayez ce qui suit:</p><ul><li>Connectez l\'appareil photo à votre ordinateur</li><li>Fermez toutes les applications tierces pouvant utiliser la caméra</li><li>Autoriser l\'accès à la caméra dans le navigateur</li></ul>","norecord":"<p><b>Problème d\'enregistrement détecté :(</b></p><p>Raisons possibles:</p><ul><li>Votre caméra ne fonctionne pas correctement</li><li>Votre navigateur ne prend pas en charge l\'API MediaRecorder</li><li>Il y a un problème avec le réseau</li></ul><p>Veuillez réessayer ou changer de navigateur / ordinateur.</p>","done":"<p><b>Vidéo enregistrée.</b></p><p>Vous pouvez réenregistrer si cette vidéo ne vous convient pas.</p>"}},"qrcode":{"text":"Scannez le code QR à l\'aide de votre smartphone, puis ouvrez le lien reçu dans le navigateur Chrome sur Android ou Safari sur iOS. Connectez votre smartphone au chargeur et positionnez la caméra de manière à ce que nous puissions voir votre lieu de travail, vous et votre ordinateur.","expires":"Le lien est valide jusqu\'à %{timeleft}"},"ready":{"title":"Vérification de l\'état de préparation","description":"Tout est prêt, vous pouvez maintenant commencer l\'événement. Si l\'événement n\'a pas pu démarrer, réessayez plus tard ou sélectionnez un autre événement.","nickname":"Nom","subject":"Titre de l\'événement","scheduled":"Heure prévue","deadline":"Date d\'expiration","error":{"ERR_SESSION_NOT_FOUND":"Aucune session active n\'est affectée à votre profil. Vous ne pouvez pas continuer.","ERR_SEB_INVALID_SIGNATURE":"Cet événement ne peut être réalisé que via le Safe Exam Browser, il n\'est pas possible de procéder via votre navigateur actuel.","ERR_NO_PROCTORS_AVAILABLE":"Il n\'y a pas de surveillants disponibles pour le moment. Veuillez réessayer plus tard.","ERR_SESSION_TIME_NOT_COME":"L\'événement n\'a pas encore commencé. Veuillez réessayer plus tard.","ERR_SESSION_TIME_EXPIRED":"L\'événement est terminé, il n\'est pas possible de continuer.","ERR_INVALID_LICENSE":"Licence invalide. Vous ne pouvez pas continuer tant que votre fournisseur n\'a pas prolongé la licence.","ERR_SERVICE_UNAVAILABLE":"Le service est temporairement indisponible, veuillez réessayer plus tard."},"button":{"start":"Démarrer"}},"chat":{"title":"Discussion","inputPlaceholder":"Saisissez votre message..."},"calculator":{"title":"Calculateur"},"conference":{"guest":"Invité","microphone":"Microphone","camera":"Appareil photo","screen":"Le partage d\'écran","mute":"Marche/arrêt volume","single":"Mode affichage","maximize":"Taille de bloc"},"vision":{"qrcode":"Connectez l\'appareil photo","events":{"b1":"Navigateur non supporté","b2":"L\'accent est passé à une autre fenêtre","b3":"Le mode plein écran est désactivé","c1":"La webcam est désactivée","c2":"Visage invisible ou vous ne regardez pas dans la caméra","c3":"Plusieurs visages devant la caméra","c4":"Le visage ne correspond pas au profil","c5":"Trouvé un profil similaire","k1":"Une écriture atypique au clavier","m1":"Le microphone est coupé ou son volume est faible","m2":"Conversation ou bruit en arrière-plan","n1":"Pas de connexion au réseau","n2":"Pas de connexion à une caméra mobile","s1":"Les activités d\'écran ne sont pas partagées","s2":"Le deuxième écran est utilisé"},"button":{"ok":"d\'accord"}},"duplicate":{"title":"Session bloquée","label":"Attention!","text":"Cette page a été ouverte ailleurs, fermez cet onglet."},"finish":{"title":"Session terminée","label":"Attention!","text":{"auto":"La session s\'est terminée automatiquement.","proctor":"La session a été interrompue par le surveillant."},"button":{"ok":"OK"}},"confirm":{"title":"Clôture de la session","label":"Terminer la session?","text":"Une fois terminé, vous ne pourrez plus continuer.","checkbox":"Je comprends et confirme l\'action","button":{"ok":"Oui","cancel":"Non"}},"iframe":{"button":{"home":"Page d\'accueil","finish":"Terminer","chat":"Discuter","calculator":"Calculatrice","qrcode":"QR Code"}}}'
            ),
          he: JSON.parse(
            '{"signup":{"title":"הרשמה לאירוע","text":"הזן את הפרמטרים של האירוע שבו ברצונך להשתתף. בדרך כלל, פרמטרים אלה מסופקים על ידי מארגן האירוע.","username":"פרטי הכניסה שלך","password":"הסיסמה שלך","template":"מזהה אירוע","error":"הפרמטרים שצוינו אינם נכונים","button":{"ok":"בסדר"}},"wizard":{"title":{"rules":"כללים והנחיות","check":"בדיקת ציוד","profile":"מילוי הפרופיל","face":"תמונת פנים","passport":"תעודה מזהה","overview":"הקלטת סקירה כללית של מקום העבודה","qrcode":"חיבור מצלמת טלפון"},"button":{"next":"הבא"},"page":"שלב %{page} מתוך %{total}"},"check":{"text":"אנא המתן בזמן שהמערכת מבצעת בדיקות, על מנת למנוע בעיות טכניות במהלך הבחינה.","empty":"בדיקת ציוד אינה נדרשת.","stage":{"browser":"בדיקת דפדפן","camera":"בדיקת מצלמת רשת","microphone":"בדיקת מיקרופון","screen":"בדיקת מסך","network":"בדיקת תקשורת ","webrtc":"WebRTC בדיקת"},"button":{"retry":"נסה שוב"},"error":{"Error":" שגיאה לא ידועה. אנא נסה שוב.","Unsupported":"הדפדפן בו הינך משתמש אינו נתמך. נסה לעדכן הדפדפן או להשתמש בדפדפן אחר.","WrongSize":"הדפדפן שלך אינו פתוח במצב תצוגה של מסך מלא. אנא עבור למצב תצוגה מסך-מלא.","NoRecorder":"MediaRecorder API אינו נתמך או כבוי. אנא אפשר שימוש ב API. עבור Settings > Safari > Advanced > Experimental Features > MediaRecorder או השתמש בדפדפן אחר.","NoWindowManagement":"לא ניתנה הרשאה לגשת למצב ריבוי מסכים. תן גישה למיקום החלונות מרובי המסכים.","NoPicture":"לא מתקבל אות וידאו מהמצלמה. נסה לסגור את התוכנות המשתמשות במצלמה ובטל את האנטיוירוס.","NoVideo":"מלצמת הרשת כבויה או אינה מותקנת. חבר מצלמה או אפשר גישה אליה.","LowVolume":"המיקרופון אינו פועל או שרמת השמע שלו נמוכה. תקן את רמת השמע או החלף מיקרופון.","NoAudio":"מיקרופון מושתק או אינו פועל. חבר את המיקרופון ואשר לדפדפו להשתמש בו.","NoCapture":"לא מתקבל אות וידאו מהממסך שלך. אפשר לדפדפן גישה למצלמה שלך.","Multiscreen":"לא שיתפת את כל המסך. אפשר את הגישה לדפדפן לכל המסך ונתק את כל הצגים הנוספים.","NoScreen":"גישה למסך שלך אינה מאופשרת או חלק מהמסך שלך חסום. אפשר לדפדפן שלך לשתף את כל המסך.","NoConnection":"תוסף כלשהו מונע גישה למערכת. נסה לכבות את חוסם הפרסומות או עבור לדפדפן אחר.","RtcError":"אין אפשרות לבסס חיבור WenRTC. נסה לכבות את חומת האש שלך והאנטיוירוס, או התחבר מרשת אינטרנט אחרת."}},"profile":{"text":"מלא או בדוק את שם המשפחה, השם הפרטי והשם האמצעי שלך (אם קיים).","lastname":"שם משפחה","firstname":"שם פרטי","middlename":"שם אמצעי","error":{"unsaved":"אירעה שגיאה במהלך שמירת הנתונים (%{code})"}},"face":{"text":"צלם תמונת פנים, מקם את הפנים במסגרת העגולה שעל המסך. וודא כי החדר בו הינך נמצא מואר היטב. אם הצילום לא מאושר, אנא נסה להצטלם שוב.","button":{"retry":"נסה שוב","take":"צלם"},"msg":{"loading":"<p><b>טוען...</b></p>","nocamera":"<p><b>זוהתה בעיה במצלמה :(</b></p><p>נסה את הצעדים הבאים:</p><ul><li>חבר את המצלמה שלך למחשב</li><li>סגור את כל התוכנות והאפליקציות המשתמשות במצלמה</li><li>אשר גישה למצלמה שלך, בדפדפן</li></ul>","noface":"<p><b>לא זיהינו אותך בתמונה :(</b></p><p>סיבות אפשריות:</p><ul><li>הפנים שלך מחוץ למסגרת </li><li>תאורה לקויה</li><li>הפנים שלך אינן מוצגות כראוי, בגלל בגד או שיער המסתיר אותן.</li><li>המצלמה נמצאת בצד או הינה ממוקת רחוק מדי ממך</li><li>מקור האור נמצא מאחריך  או מהצד</li></ul><p>נסה להצלם מחדש.</p>","unverified":"<p><b>גישה לא אושרה :(</b></p><p>תמונתך אינה תואמת את תמונת הפרופיל שלך.</p>","done":"<p><b>צילום נשמר.</b></p><p>תוכל להצטלם מחדש אם תרצה.</p>"}},"passport":{"text":{"photo":"צלם את תעודת הסטודנט שלך, כך שהתמונה והשם שלך מוצגים בצורה ברורה.","scan":"פורמט ההעלאה של המסמך הוא JPEG או PNG. הוסף סריקה של כרטיס הסטודנט שלך. ודא כי התמונה והשם שלך מוצגים בצורה ברורה.","both":"פורמט ההעלאה של המסמך הוא JPEG או PNG. צלם תמונה אן הוסף סריקה של תעודת הסטודנט שלך. ודא כי התמונה והשם שלך מוצגים בצורה ברורה."},"textExtra":{"photo":"צלם תמונה של דף אחר של המזהה שלך.","scan":"הורד סריקה של דף אחר של המזהה שלך. התבנית של מסמך JPEG או PNG להורדה.","both":"צלם או העלה סריקה של דף אחר של המזהה שלך. התבנית של מסמך JPEG או PNG להורדה."},"button":{"retry":"נסה שוב","take":"צלם","upload":"העלה","add":"1+ לתמונה","reset":"אִתחוּל"},"msg":{"loading":"<p><b>טוען...</b></p>","ready":"<p><b>אנא עקבו אחר הדרישות הבאות:</b></p><ul><li>קובץ בפורמט JPEG או PNG</li><li>גודל קובץ מירבי 5 MB</li><li>רזולוציה מינימלית של 1 Mpix</li><li>קובץ אופקי</li><li>על המסמך להכיל תמונה אחת</li><li>יש לוודא כי הטקסט והתמונה מוצגים וניתנים לזיהוי בבירור</li></ul>","nocamera":"<p><b>זוהתה בעיה עם מצלמת הרשת :(</b></p><p>נסה את הצעדים הבאים:</p><ul><li>חבר את המצלמה למחשב</li><li>סגור כל תוכנה או אפליקציה המשתמשת במצלמה</li><li>אשר לדפדפן שלך שימוש וגישה למצלמה</li></ul>","nophoto":"<p><b>לא זוהה מסמך בתמונה :(</b></p><p>סיבות אפשריות:</p><ul><li>המסמך לא נכנס באופן מלא למסגרת </li><li>המסמך אינו אופקי</li><li>התמונה המזהה במסמך אינה ברורה</li><li>הטקסט במסמך אינו קריא</li><li>`%{nickname}` השם לא תואם</li></ul><p>נסו לצלם את התמונה שוב.</p>","noscan":"<p><b>המסמך לא מזוהה בסריקה :(</b></p><p>סיבות אפשריות:</p><ul><li>הקובץ אינו בפורמט JPEG או PNG</li><li>גודלו של הקבוץ הינו יותר מ 5 MB</li><li>רזולוצית הקובץ קטנה מ 1 Mpix</li><li>המסמך אינו אופקי</li><li>התמונה המזהה או הטקסט אינם קריאים או ברורים</li><li>`%{nickname}` השם לא תואם</li></ul><p>נסה להעלות קובץ אחר.</p>","unverified":"<p style=\\";text-align:right;direction:rtl\\"><b>גישה נדחתה :(</b></p><p style=\\";text-align:right;direction:rtl\\"> המסמך אינו תואם למסמך בפרופיל החבר.</p>","taken":"<p><b>התמונה נשמרה.</b></p><p>אם אינך מרוצה מהתמונה, תוכל לצלם אות המחדש.</p>","uploaded":"<p><b>המסמך הסרוק הועלה.</b></p><p>אם אינך מרוצה מהתמונה, תוכל להעלות את הקובץ שוב.</p>"}},"overview":{"text":"הקלט סרטון קצר המציג את סביבת העבודה שלך באמצעות מצלמת המחשב או מצלמת הטלפון החכם. אם אתה משתמש בסמארטפון, סרוק את קוד ה-QR באמצעות הטלפון החכם שלך ולאחר מכן פתח את הקישור שהתקבל בדפדפן Chrome ב-Android או Safari ב-iOS.","expires":"הקישור פעיל עד %{timeleft}","button":{"retry":"נסה שוב","start":"התחל להקליט","stop":"הפסק להקליט","save":"להציל","qrcode":"קוד QR"},"msg":{"loading":"<p><b>טוען...</b></p>","nocamera":"<p><b>זוהתה בעיה עם מצלמת הרשת :(</b></p><p>נסה את הצעדים הבאים:</p><ul><li>חבר את המצלמה למחשב</li><li>סגור כל תוכנה או אפליקציה המשתמשת במצלמה</li><li>אשר לדפדפן שלך שימוש וגישה למצלמה</li></ul>","norecord":"<p><b>זוהתה בעיה בהקלטה :(</b></p><p>סיבות אפשריות:</p><ul><li>המצלמה שלך לא פועלת כמו שצריך</li><li>הדפדפן שלך אינו תומך ב-MediaRecorder API</li><li>יש בעיה ברשת</li></ul><p>אנא נסה שוב או שנה את הדפדפן / המחשב שלך.</p>","done":"<p><b>הסרטון נשמר.</b></p><p>אתה יכול להקליט מחדש אם הסרטון הזה לא מתאים לך.</p>"}},"qrcode":{"text":"סרוק את קוד ה-QR באמצעות הטלפון החכם שלך ולאחר מכן פתח את הקישור שהתקבל בדפדפן Chrome ב-Android או ב-Safari ב-iOS. חבר את הסמארטפון שלך למטען ומקם את המצלמה כך שנוכל לראות את מקום העבודה שלך, אותך ואת המחשב שלך.","expires":"הקישור פעיל עד %{timeleft}"},"ready":{"title":"בדיקת מוכנות","description":"הכל מוכן, עכשיו אתה יכול להתחיל את האירוע. אם האירוע לא הצליח להתחיל, נסה שוב מאוחר יותר או בחר אירוע אחר.","nickname":"שֵׁם","subject":"כותרת האירוע","scheduled":"זמן מתוכנן","deadline":"תאריך תפוגה","error":{"ERR_SESSION_NOT_FOUND":"לפרופיל שלך לא הוקצה שום פעילות פעילה. אתה לא יכול להמשיך.","ERR_SEB_INVALID_SIGNATURE":"אירוע זה יכול להתבצע רק דרך ה- Safe Exam Browser, לא ניתן להמשיך דרך הדפדפן הנוכחי שלך.","ERR_NO_PROCTORS_AVAILABLE":"כרגע אין פרוקטורים זמינים. בבקשה נסה שוב מאוחר יותר.","ERR_SESSION_TIME_NOT_COME":"האירוע עדיין לא התחיל. בבקשה נסה שוב מאוחר יותר.","ERR_SESSION_TIME_EXPIRED":"האירוע הסתיים, לא ניתן להמשיך.","ERR_INVALID_LICENSE":"רישיון לא חוקי. אינך יכול להמשיך עד שהספק שלך האריך את הרישיון.","ERR_SERVICE_UNAVAILABLE":"השירות אינו זמין באופן זמני. נסה שוב מאוחר יותר."},"button":{"start":"הַתחָלָה"}},"chat":{"title":"צ\'אט","inputPlaceholder":"הקלד טקסט כאן..."},"calculator":{"title":"מַחשְׁבוֹן"},"conference":{"guest":"אורח","microphone":"מיקרופון","camera":"מצלמה","screen":"שיתוף מסך","mute":"קול מופעל/כבוי","single":"אפשרויות תצוגה","maximize":"גודל משבצת"},"vision":{"qrcode":"חבר את מצלמת האינטרנט שלך","events":{"b1":"דפדפן לא נתמך","b2":"פוקוס עבר לחלון אחר","b3":"בוטל מצב מסך מלא","c1":"מצלמה כובתה","c2":"פנים מוסתרות או אינן מביטות הישר למצלמה","c3":"זוהו מספר פנים במצלמה","c4":"פנים אינן תואמות לפרופיל המשתמש","c5":"נמצא פרופיל דומה","k1":"הקלדה לא טיפוסית במקלדת","m1":"מיקרופון מושתק או אינו פעיל","m2":"זוהה רעש או שיחה ברקע","n1":"אין חיבור לאינטרנט","n2":"אין חיבור למצלמת הטלפון","s1":"שיתוף מסך אינו פועל","s2":"זוהה שימוש במסך נוסף"},"button":{"ok":"אישור"}},"duplicate":{"title":"הנסיון נחסם","label":"שים לב!","text":"העמוד נפתח במקום אחר, סגור את הלשונית הזו"},"finish":{"title":"נסיון הושלם","label":"שים לב!","text":{"auto":"הנסיון ננעל באופן אוטומטי.","proctor":"הנסיון הופסק על ידי המשגיח"},"button":{"ok":"אישור"}},"confirm":{"title":"סיום הבחינה","label":"לסיים את ההגשחה והבחינה?","text":"האם סיימת והגשת את הבחינה? יש ללחוץ על סיום רק לאחר הגשת הבחינה","checkbox":"אני מבין ומאשר את הפעולה","button":{"ok":"אישור","cancel":"ביטול"}},"iframe":{"button":{"home":"עמוד הבית","finish":"סיום הניטור והבחינה","chat":"לְשׂוֹחֵחַ","calculator":"מַחשְׁבוֹן","qrcode":"קוד QR"}}}'
            ),
          kk: JSON.parse(
            '{"signup":{"title":"Іс-шараға тіркелу","text":"Қатысқыңыз келетін іс-шараның параметрлерін енгізіңіз. Әдетте, бұл параметрлерді іс-шара ұйымдастырушысы ұсынады.","username":"Сіздің логиніңіз","password":"Құпия сөзіңіз","template":"Оқиға идентификаторы","error":"Көрсетілген параметрлер дұрыс емес","button":{"ok":"ЖАҚСЫ"}},"wizard":{"title":{"rules":"Іс-шараны өткізу шарттары","check":"Жабдықты тексеру","profile":"Профильді толтыру","face":"Бет жүзді суретке түсіру","passport":"Жеке тұлғаны куәландыратын құжатты жүктеу","overview":"Жұмыс орнын шолуды жазу","qrcode":"Ұялы телефон камерасын қосу"},"button":{"next":"Әрі қарай"},"page":"%{page} қадам %{total} ішінен"},"check":{"text":"Болуы мүмкін техникалық мәселелер іс-шараға кедергі келтірмеуі үшін, жүйе компьютер мен желіні тексергенше күтіңіз.","empty":"Тексеріс қажет емес.","stage":{"browser":"Браузерді тексеру","camera":"Веб-камераны тексеру","microphone":"Микрофонды тексеру","screen":"Экранды тексеру","network":"Қосылымды тексеру","webrtc":"WebRTC тексеру"},"button":{"retry":"Қаталау"},"error":{"Error":"Белгісіз қате. тексеруді қайтадан қайталап көріңіз.","Unsupported":"Сіздің браузеріңізге немесе құрылғыңызға қолдау көрсетілмейді. Басқа браузерді қолданып көріңіз немесе құрылғыны ауыстырыңыз.","WrongSize":"Браузер терезесі толық экранға шығарылмаған. Оны кеңейтіңіз немесе толық экран режиміне өтіңіз.","NoRecorder":"MediaRecorder API қолдауы жоқ немесе өшірулі. Бұл API-ді қосыңыз (Баптаулар > Safari > Қосымшалар > Experimental Features > MediaRecorder) немесе басқа браузерді пайдаланыңыз.","NoWindowManagement":"Көп экранды режимге кіруге рұқсат берілмейді. Көп экранды терезенің орналасуына рұқсат беріңіз.","NoPicture":"Камерадан бейне жоқ. Барлық үшінші тарап қолданбаларын жауып, антивирусты өшіріп көріңіз, браузердегі камераның жұмысын тексеріңіз.","NoVideo":"Веб-камера жұмыс істемейді немесе оған қосылу мүмкін емес. Камераны қосыңыз және оған браузерден кіруге рұқсат етіңіз, браузердегі камераның жұмысын тексеріңіз.","LowVolume":"Микрофонда ақау бар немесе дыбыс деңгейі төмен. Микрофонның дыбыс деңгейін реттеңіз немесе оны ауыстырыңыз.","NoAudio":"Микрофон өшірілген немесе оған қосылу мүмкін емес. Микрофонды қосыңыз және оған браузерден қосылуға рұқсат беріңіз, браузердегі микрофонның жұмысын тексеріңіз.","NoCapture":"Экраннан бейне жоқ. Экранға қосылу мүмкіндігін жаппаңыз.","Multiscreen":"Сіз бүкіл экранды бөліскен жоқсыз. Егер қосылған болса, қосымша дисплейлерді өшіріп, бүкіл экранға қол жеткізу мүмкіндігін қосыңыз.","NoScreen":"Экранға қол жетімділік жоқ немесе экранның тек бір бөлігі қол жетімді. Бүкіл экранға қосылуға рұқсат беріңіз.","NoConnection":"WebSocket қосылымы бұғатталған. AdBlock жарнама блокаторын немесе соған ұқсас браузер кеңейтімдерін өшіріп көріңіз.","RtcError":"WebRTC қосылымын орнату мүмкін емес. Брандмауэр мен антивирусты өшіріп көріңіз немесе басқа желіге қосылыңыз."}},"profile":{"text":"Тегі, аты және әкесінің аты (бар болса) толтырыңыз немесе тексеріңіз.","lastname":"Тек","firstname":"Аты","middlename":"Әкесінің аты","error":{"unsaved":"Деректерді сақтау кезінде қате орын алды (%{code})"}},"face":{"text":"Бетіңіз экрандағы сопақша кеңістікке сиятындай етіп суретке түсіңіз. Бет жүзіңіз біркелкі жарықтандырылып, толығымен көрінуі керек. Егер сурет дұрыс болма қалса, суретке қайта түсіріңіз.","button":{"retry":"Қайталау","take":"Суретке түсіру"},"msg":{"loading":"<p><b>Жүктелуде...</b></p>","nocamera":"<p><b>Веб-камерада мәселе анықталды :(</b></p><p>Келесі әрекеттерді орындап көріңіз:</p><ul><li>Камераны компьютерге қосыңыз</li><li>Камераны қолдана алатын үшінші тарап бағдарламаларын өшіріңіз</li><li>Браузерде камераға қосылу мүмкіндігін қосыңыз</li></ul>","noface":"<p><b>Суретте сізді таппадық:(</b></p><p>Ықтимал себептер:</p><ul><li>Бет жүзіңіз кадрға түспей қалған</li><li>Жарықтандырудың нашар болуы</li><li>Киімнің немесе шашыңыздың кесірінен бетіңіз көрінбей қалды</li><li>Камера сіздің жаныңызда немесе тым алыс орналасқан</li><li>Жарық көзі сіздің артыңызда немесе жаныңызда орналасқан</li></ul><p>Суретке тағы бір рет түсіп көріңіз.</p>","unverified":"<p><b>Кіруге тыйым салынған :(</b></p><p>Тұлғаның суреті қатысушы профильдегі суретке сәйкес келмейді.</p>","done":"<p><b>Сурет сақталды.</b></p><p>Егер сурет көңіліңізден шықпаса, қайта түсіріп көрсеңіз болады.</p>"}},"passport":{"text":{"photo":"Фотосуретіңіз бен есіміңіз көрсетілген жеке куәлігіңіздің парағын суретке түсіріңіз.","scan":"Жеке куәлігіңіздің бір бетінің сканын жүктеңіз, онда сіздің фотосуреттеріңіз бен атыңыз болуы тиіс. Жүктелетін құжат пішімі JPEG немесе PNG.","both":"Фотосуретіңіз бен атыңыз көрсетілген жеке басыңызды куәландыратын құжатыңыздың сканерленген парағын жүктеңіз немесе суретке түсіріңіз. Жүктелетін құжат пішімі JPEG немесе PNG."},"textExtra":{"photo":"Жеке куәлігіңіздің басқа бетін суретке түсіріңіз.","scan":"Жеке куәлігіңіздің басқа бетінің сканерін жүктеп салыңыз. Жүктеп салынған құжаттың пішімі JPEG немесе PNG болып табылады.","both":"Жеке куәлігіңіздің басқа бетін фотосуретке түсіріңіз немесе сканерлеңіз. Жүктеп салынған құжаттың пішімі JPEG немесе PNG болып табылады."},"button":{"retry":"Қайталау","take":"Суретке түсіру","upload":"Жүктеу","add":"+1 фото","reset":"Қалпына келтіру"},"msg":{"loading":"<p><b>Жүктелуде...</b></p>","ready":"<p><b>Келесі талаптарды сақтаңыз:</b></p><ul><li>Файл пішімі JPEG немесе PNG</li><li>Файл көлемі 5 МБ артық болмауы тиіс</li><li>Сурет ажыратылымдығы 1 Мпикс кем болмауы тиіс</li><li>Файл бағдары көлденең болу керек</li><li>Құжатта тек бір ғана фотосурет болу керек</li><li>Мәтін мен фотосурет дұрыс көрінуі тиіс</li></ul>","nocamera":"<p><b>Веб-камерада мәселе анықталды :(</b></p><p>Келесі әрекеттерді орындап көріңіз:</p><ul><li>Камераны компьютерге қосыңыз</li><li>Камераны қолдана алатын үшінші тарап бағдарламаларын өшіріңіз</li><li>Браузерде камераға қосылу мүмкіндігін қосыңыз</li></ul>","nophoto":"<p><b>Суретте құжат табылмады :(</b></p><p>Ықтимал себептер:</p><ul><li>Құжат кадрға толық сыймай қалды</li><li>Құжат бағыты көлденең орналаспаған</li><li>Құжаттағы фотосурет нашар көрінеді</li><li>Құжаттағы мәтін нашар көрінеді</li><li>Аты сәйкес емес `%{nickname}`</li></ul><p>Суретке қайта түсіріп көріңіз.</p>","noscan":"<p><b>Сканда құжат табылмады :(</b></p><p>Ықтимал себептер:</p><ul><li>Файл JPEG немесе PNG пішіміне сәйкес емес</li><li>Файл көлемі 5 МБ асып кетті</li><li>Сурет ажыратылымдығы 1 Мпикс кем</li><li>Құжат бағдары көлденең емес</li><li>Фотосурет немесе мәтін дұрыс көрінбейді</li><li>Аты сәйкес емес `%{nickname}`</li></ul><p>Басқа файл жүктеп көріңіз.</p>","unverified":"<p><b>Рұқсат жоқ :(</b></p><p> Құжат мүше профиліндегі құжатқа сәйкес келмейді.</p>","taken":"<p><b>Сурет сақталды.</b></p><p>Егер сурет көңіліңізден шықпаса, қайта түсіріп көрсеңіз болады.</p>","uploaded":"<p><b>Құжат сканы жүктелді.</b></p><p>Егер сурет көңіліңізден шықпаса, файлды қайта жүктеп көрсеңіз болады.</p>"}},"overview":{"text":"Компьютер камерасы немесе смартфон камерасы арқылы жұмыс кеңістігіңізді көрсететін қысқа бейне түсіріңіз. Смартфонды пайдалансаңыз, смартфон арқылы QR кодын сканерлеңіз, содан кейін алынған сілтемені Android жүйесінде Chrome браузерінде немесе iOS жүйесінде Safari арқылы ашыңыз.","expires":"Сілтеме %{timeleft} дейін жарамды","button":{"retry":"Қайталау","start":"Жазуды бастаңыз","stop":"Жазуды тоқтату","save":"Сақтау","qrcode":"QR коды"},"msg":{"loading":"<p><b>Жүктелуде...</b></p>","nocamera":"<p><b>Веб-камерада мәселе анықталды :(</b></p><p>Келесі әрекеттерді орындап көріңіз:</p><ul><li>Камераны компьютерге қосыңыз</li><li>Камераны қолдана алатын үшінші тарап бағдарламаларын өшіріңіз</li><li>Браузерде камераға қосылу мүмкіндігін қосыңыз</li></ul>","norecord":"<p><b>Жазу кезінде ақау анықталды :(</b></p><p>Ықтимал себептер:</p><ul><li>Камераңыз дұрыс жұмыс істемейді</li><li>Браузеріңіз MediaRecorder API қолданбасын қолдамайды</li><li>Желіде ақау бар</li></ul><p>Қайталап көріңіз немесе браузеріңізді / компьютеріңізді өзгертіңіз.</p>","done":"<p><b>Бейне сақталды.</b></p><p>Бұл бейне сізге сәйкес келмесе, қайта жазуыңызға болады.</p>"}},"qrcode":{"text":"Смартфон арқылы QR кодын сканерлеңіз, содан кейін алынған сілтемені Android жүйесінде Chrome браузерінде немесе iOS жүйесінде Safari арқылы ашыңыз. Смартфонды зарядтағышқа қосып, камераны жұмыс орныңызды, сізді және компьютеріңізді көре алатындай етіп орналастырыңыз.","expires":"Сілтеме %{timeleft} дейін жарамды"},"ready":{"title":"Дайындықты тексеру","description":"Барлығы дайын, енді іс-шараны бастауға болады. Егер іс-шараны бастау мүмкін болмаса, оны кейінірек жасауға тырысыңыз.","nickname":"Аты","subject":"Атауы","scheduled":"Кірудің басталуы","deadline":"Кірудің аяқталуы","error":{"ERR_SESSION_NOT_FOUND":"Қазіргі уақытта сізде бірде-бір белсенді сеанс жоқ, сіз жалғастыра алмайсыз.","ERR_SEB_INVALID_SIGNATURE":"Бұл іс-шараға тек Safe Exam Browser браузері арқылы ғана кіру рұқсат етіледі, сіз бұл браузерде жалғастыра алмайсыз.","ERR_NO_PROCTORS_AVAILABLE":"Қазіргі уақытта бос прокторлар жоқ, кейінірек қайталап көріңіз.","ERR_SESSION_TIME_NOT_COME":"Іс-шараңыздың уақыты әлі келген жоқ, кейінірек қайталап көріңіз.","ERR_SESSION_TIME_EXPIRED":"Іс-шараңыздың уақыты өтті, сіз әрі қарай жалғастыра алмайсыз.","ERR_INVALID_LICENSE":"Лицензия жарамсыз, вендор лицензияны ұзартқанша сіз әрі қарай жалғастыра алмайсыз.","ERR_SERVICE_UNAVAILABLE":"Қызмет уақытша қол жетімсіз, кейінірек қайталап көріңіз."},"button":{"start":"Бастау"}},"chat":{"title":"Чат","inputPlaceholder":"Хабарлама мәтінін енгізіңіз..."},"calculator":{"title":"Калькулятор"},"conference":{"guest":"Қонақ","microphone":"Микрофон","camera":"Камера","screen":"Экранды көрсету","mute":"Дыбысты қосу/өшіру","single":"Көрсету режимі","maximize":"Блок өлшемі"},"vision":{"qrcode":"Ұялы телефон камерасын қосыңыз","events":{"b1":"браузерге қолдау көрсетілмейді","b2":"Фокус үшінші тарап қосымшасына аударылды","b3":"Браузер терезесі толық экранға ашылмаған","c1":"камера жұмыс істемейді","c2":"камераға бетіңіз дұрыс көрінбей тұр","c3":"бөтен адам байқалды","c4":"Камера алдындағы тұлға профильге сәйкес келмейді","c5":"Тұлғаның басқа профильмен ұқсастығы анықталды","k1":"Әдеттегідей емес пернетақталық қолтаңба анықталды","m1":"Микрофон өшірулі немесе жұмыс істемейді","m2":"фондық шу немесе әңгіме естіледі","n1":"желілік байланыс мәселесі","n2":"Ұялы телефон камерасының қосылу мәселесі","s1":"Экраннан видео жоқ","s2":"Қосымша монитор қолданылады"},"button":{"ok":"OK"}},"duplicate":{"title":"Сеанс бұғатталған","label":"Назар аударыңыз!","text":"Осы парақша басқа жерде ашылды, бұл бетті жабыңыз."},"finish":{"title":"Сеанс аяқталды","label":"Назар аударыңыз!","text":{"auto":"Сеанс автоматты түрде аяқталды.","proctor":"Сеанс проктор тарапынан аяқталды."},"button":{"ok":"OK"}},"confirm":{"title":"Сеансты аяқтау","label":"Сеансты аяқтау керек пе?","text":"Аяқтағаннан кейін сіз әрі қарай жалғастыра алмайсыз.","checkbox":"Мен әрекетті түсінемін және растаймын","button":{"ok":"Иә","cancel":"Жоқ"}},"iframe":{"button":{"home":"Бастапқы парақша","finish":"Аяқтау","chat":"Чат","calculator":"Калькулятор","qrcode":"QR коды"}}}'
            ),
          lv: JSON.parse(
            '{"signup":{"title":"Reģistrācija pasākumam","text":"Ievadiet tā pasākuma parametrus, kurā vēlaties piedalīties. Parasti šos parametrus nodrošina pasākuma organizators.","username":"Jūsu pieteikšanās","password":"Tava parole","template":"Notikuma identifikators","error":"Norādītie parametri ir nepareizi","button":{"ok":"LABI"}},"wizard":{"title":{"rules":"Noteikumi","check":"Iekārtas pārbaude","profile":"Profila aizpildīšana","face":"Sejas fotografēšana","passport":"Personas dokumenta augšupielāde","overview":"Darba vietas pārskata ierakstīšana","qrcode":"Mobilās kameras savienojums"},"button":{"next":"Nākamais"},"page":"Solis %{page} no %{total}"},"check":{"text":"Uzgaidiet, kamēr sistēma pārbauda datoru un tīklu, lai iespējamās tehniskās problēmas neaizkavētu sesijas norisi.","empty":"Pārbaude nav nepieciešama.","stage":{"browser":"Pārlūkprogramma pārbaudīta","camera":"Web-kamera pārbaudīta","microphone":"Mikrofons pārbaudīts","screen":"Ekrāns pārbaudīts","network":"Savienojums pārbaudīts","webrtc":"WebRTC pārbaude"},"button":{"retry":"Atkārtot pārbaudi"},"error":{"Error":" Nezināma kļūda. Lūdzu, mēģiniet vēlreiz.","Unsupported":"Jūsu pārlūks netiek atbalstīts. Atjauniniet savu pārlūkprogrammu vai izmantojiet citu pārlūku.","WrongSize":"Pārlūka logs nav pilnekrāna režīmā. Lūdzu, pārslēdzieties uz pilnekrāna režīmu.","NoRecorder":"MediaRecorder API netiek atbalstīta vai ir atspējota. Lūdzu, iespējojiet šo API vai izmantojiet citu pārlūkprogrammu.","NoWindowManagement":"Nav piešķirta atļauja piekļūt vairāku ekrānu režīmam. Piešķiriet piekļuvi vairāku ekrānu logu izvietojumam.","NoPicture":"Nepienāk video signāls no kameras. Mēģiniet aizvērt visas citas programmas un atspējot antivīrusa programmu.","NoVideo":"Tīmekļa kamera ir atspējota vai nav atrasta. Pievienojiet web-kameru vai izmantojiet mobilā telefona kameru","LowVolume":"Mikrofonam ir noslēgts skaļums vai tas nedarbojas. Paaugstiniet skaļumu vai nomainiet mikrofonu.","NoAudio":"Mikrofons ir izslēgts vai atspējots. Pievienojiet mikrofonu un iespējojiet pārlūka piekļuvi mikrofonam.","NoCapture":"Nav ekrāna video. Iespējojiet pārlūka piekļuvi kamerai.","Multiscreen":"Jūs neesat kopīgojis visu ekrānu. Iespējojiet pārlūkprogrammas piekļuvi visam ekrānam un atvienojiet visus papildu displejus.","NoScreen":"Piekļuve ekrānam ir atspējota vai daļa ekrāna ir bloķēta. Iespējojiet pārlūka piekļuvi visam ekrānam.","NoConnection":"Savienojums ir bloķēts. Mēģiniet atspējot reklāmu bloķētāju kā AdBlock vai līdzīgus pārlūka paplašinājumus.","RtcError":"Nevar izveidot WebRTC savienojumu. Mēģiniet izslēgt ugunsmūri un antivīrusu vai izveidot savienojumu ar citu tīklu."}},"profile":{"text":"Aizpildiet vai pārbaudiet savu uzvārdu, vārdu un otro vārdu (ja pieejams).","lastname":"Uzvārds","firstname":"Vārds","middlename":"Otrais vārds","error":{"unsaved":"Saglabājot datus, radās kļūda (%{code})"}},"face":{"text":"Uzņemiet sejas fotoattēlu, kas ietilpst ovālajā rāmī uz ekrāna. Pārliecinieties, vai telpā ir pietiekami daudz gaismas. Ja fotoattēls nav akceptēts, lūdzu, mēģiniet vēlreiz.","button":{"retry":"Mēģināt vēlreiz","take":"Uzņemt foto"},"msg":{"loading":"<p><b>Uzgaidiet...</b></p>","nocamera":"<p><b>Tika atklāta problēma ar tīmekļa kameru :(</b></p><p>Mēģiniet šo:</p><ul><li>Pievienojiet kameru datoram</li><li>Aizveriet visas citas programmas, kuras var izmantot kameru.</li><li>Pārlūkā ļaujiet piekļūt kamerai</li></ul>","noface":"<p><b>Sejas fotoattēls nav atpazīts :(</b></p><p>Iespējamie iemesli:</p><ul><li>Seja ir ārpus rāmja</li><li>Vājš apgaismojums</li><li>Seja ir aizklāta ar matiem vai drēbēm</li><li>Kamera ir apgriesta uz sāniem vai ir pārāk tālu</li><li>Aiz muguras vai no sāniem spīd spoža gaisma</li></ul><p>Mēģiniet attēlu uzņemt atāktoti.</p>","unverified":"<p><b>Piekļuve liegta :(</b></p><p>Uzņemtais attēls neatbilst tavai identitātei/profilam.</p>","done":"<p><b>Foto saglabāts.</b></p><p>Tu vari attēlu uzņemt atkārtoti, ja tas nav atbilstošs.</p>"}},"passport":{"text":{"photo":"Uzņemiet personu apliecinoša dokumenta attēlu, kurā skaidri redzams jūsu fotoattēls un vārds.","scan":"Augšupielādējiet personas dokumenta skenēšanu, kurā skaidri redzams jūsu fotoattēls un vārds. Augšupielādētā dokumenta formāts ir JPEG vai PNG.","both":"Uzņemiet attēlu vai augšupielādējiet personas dokumenta skenēšanu, kurā skaidri redzams jūsu fotoattēls un vārds. Augšupielādētā dokumenta formāts ir JPEG vai PNG."},"textExtra":{"photo":"Nofotografējiet savu personu apliecinošā dokumenta otru lapu.","scan":"Augšupielādējiet vēl vienas sava personu apliecinoša dokumenta lapas skenējumu. Augšupielādējamā dokumenta formāts ir JPEG vai PNG.","both":"Uzņemiet fotoattēlu vai augšupielādējiet skenētu citu personu apliecinoša dokumenta lapu. Augšupielādējamā dokumenta formāts ir JPEG vai PNG."},"button":{"retry":"Mēģināt vēlreiz","take":"Uzņemt foto","upload":"Augšupielādēt","add":"+1 fotoattēls","reset":"Atiestatīt"},"msg":{"loading":"<p><b>Uzgaidiet...</b></p>","ready":"<p><b>Lūdzu, ievērojiet prasības:</b></p><ul><li>Faila formāts JPEG vai PNG</li><li>Faila lielums nedrīkst pārsniegt 5 MB</li><li>Attēla izšķirtspēja nav mazāka par 1 Mpix</li><li>Horizontāls fails</li><li>Dokumentā jābūt vienam fotoattēlam</li><li>Tekstam un fotoattēlam jābūt skaidri atpazīstamam</li></ul>","nocamera":"<p><b>Konstatēta problēma ar tīmekļa kameru :(</b></p><p>Lūdzu, izmēģiniet sekojošo:</p><ul><li>Pievienojiet kameru datoram</li><li>Aizveriet visas trešo pušu programmas, kuras var izmantot kameru</li><li>Atļaut piekļuvi kamerai pārlūkprogrammā</li></ul>","nophoto":"<p><b>Attēlā dokuments nav atrasts :(</b></p><p>Iespējamie iemesli:</p><ul><li>Dokuments pilnībā neietilpst rāmī</li><li>Dokuments nav horizontāls</li><li>Foto dokumentā nav skaidrs</li><li>Dokumenta tekstu nevar atpazīt</li><li>Vārds neatbilst `%{nickname}`</li></ul><p>Mēģiniet fotografēt vēlreiz.</p>","noscan":"<p><b>Skenēšanas laikā dokuments nav atklāts :(</b></p><p>Iespējamie iemesli:</p><ul><li>Fails nav JPEG vai PNG formāts</li><li>Faila lielums ir lielāks par 5 MB</li><li>Attēla izšķirtspēja ir mazāka par 1 Mpix</li><li>Dokuments nav horizontāls</li><li>Fotoattēls vai teksts dokumentā nav skaidrs</li><li>Vārds neatbilst `%{nickname}`</li></ul><p>Mēģiniet augšupielādēt citu failu.</p>","unverified":"<p><b>Pieeja noliegta :(</b></p><p> Dokuments neatbilst dokumentam dalībnieka profilā.</p>","taken":"<p><b>Attēls ir saglabāts.</b></p><p>Ja esat neapmierināts ar attēlu, varat to atkārtoti uzņemt.</p>","uploaded":"<p><b>Skenētais dokuments ir augšupielādēts.</b></p><p>Ja neapmierina attēls, varat failu augšupielādēt vēlreiz.</p>"}},"overview":{"text":"Izmantojot datora kameru vai viedtālruņa kameru, ierakstiet īsu video, kurā parādīta jūsu darbvieta. Ja izmantojat viedtālruni, skenējiet QR kodu, izmantojot viedtālruni, un pēc tam atveriet saņemto saiti pārlūkprogrammā Chrome operētājsistēmā Android vai Safari operētājsistēmā iOS.","expires":"Saite ir aktīva vēl %{timeleft}","button":{"retry":"Mēģināt vēlreiz","start":"Sāciet ierakstīšanu","stop":"Pārtraukt ierakstīšanu","save":"Saglabāt","qrcode":"QR kods"},"msg":{"loading":"<p><b>Uzgaidiet...</b></p>","nocamera":"<p><b>Konstatēta problēma ar tīmekļa kameru :(</b></p><p>Lūdzu, izmēģiniet sekojošo:</p><ul><li>Pievienojiet kameru datoram</li><li>Aizveriet visas trešo pušu programmas, kuras var izmantot kameru</li><li>Atļaut piekļuvi kamerai pārlūkprogrammā</li></ul>","norecord":"<p><b>Konstatēta problēma ar ierakstīšanu :(</b></p><p>Iespējamie iemesli:</p><ul><li>Jūsu kamera nedarbojas pareizi</li><li>Jūsu pārlūkprogramma neatbalsta MediaRecorder API</li><li>Radās problēma ar tīklu</li></ul><p>Lūdzu, mēģiniet vēlreiz vai mainiet pārlūkprogrammu / datoru.</p>","done":"<p><b>Videoklips saglabāts.</b></p><p>Varat ierakstīt atkārtoti, ja šis videoklips jums nav piemērots.</p>"}},"qrcode":{"text":"Skenējiet QR kodu, izmantojot viedtālruni, un pēc tam atveriet saņemto saiti pārlūkprogrammā Chrome operētājsistēmā Android vai Safari operētājsistēmā iOS. Pievienojiet viedtālruni lādētājam un novietojiet kameru tā, lai mēs varētu redzēt jūsu darba vietu, jūs un datoru.","expires":"Saite ir aktīva vēl %{timeleft}"},"ready":{"title":"Gatavības pārbaude","description":"Viss ir gatavs, tagad varat sākt pasākumu. Ja pasākumu nevarēja sākt, vēlāk mēģiniet vēlreiz vai atlasiet citu notikumu.","nickname":"Nosaukums","subject":"Pasākuma nosaukums","scheduled":"Plānotais laiks","deadline":"Derīguma termiņš","error":{"ERR_SESSION_NOT_FOUND":"Jūsu profilam nav piešķirta neviena aktīva sesija. Jūs nevarat turpināt.","ERR_SEB_INVALID_SIGNATURE":"Šo pasākumu var veikt tikai caur Safe Exam Browser, nav iespējams turpināt ar pašreizējo pārlūkprogrammu.","ERR_NO_PROCTORS_AVAILABLE":"Šobrīd nav pieejamu prokuroru. Lūdzu, pamēģiniet vēlreiz vēlāk.","ERR_SESSION_TIME_NOT_COME":"Pasākums vēl nav sācies. Lūdzu, pamēģiniet vēlreiz vēlāk.","ERR_SESSION_TIME_EXPIRED":"Pasākums ir pabeigts, to nav iespējams turpināt.","ERR_INVALID_LICENSE":"Nederīga licence. Jūs nevarat turpināt, kamēr jūsu pārdevējs nav pagarinājis licences termiņu.","ERR_SERVICE_UNAVAILABLE":"Pakalpojums īslaicīgi nav pieejams. Lūdzu, vēlāk mēģiniet vēlreiz."},"button":{"start":"Sākt"}},"chat":{"title":"Sarakste","inputPlaceholder":"Ievadiet ziņojumu..."},"calculator":{"title":"Kalkulators"},"conference":{"guest":"Viesis","microphone":"Mikrofons","camera":"Kamera","screen":"Ekrāna kopīgošana","mute":"Ieslēgt/Izslēgt skaņu","single":"Ekrāna režīms","maximize":"Izmērs"},"vision":{"qrcode":"Pievienojiet mobilā tālruņa kameru","events":{"b1":"Pārlūkprogramma netiek atbalstīta","b2":"Ir atvērts cits logs","b3":"Atspējots pilnekrāns","c1":"Atslēgta web-kamera","c2":"Seja nav redzama kamerā","c3":"Ir atpazītas vairāk kā 2 sejas","c4":"Seja neatbilst ID/attēlam","c5":"Atrasts līdzīgs profils","k1":"Netipisks tastatūras rokraksts","m1":"Izslēgta vai pazemināta mikrofona skaņa","m2":"Ir konstatēta fona saruna vai skaņa","n1":"Nav interneta savienojuma","n2":"Zaudēts savienojums ar kameru","s1":"Ekrāna aktivitātes netiek kopīgotas","s2":"Tiek izmantots otrs ekrāns"},"button":{"ok":"OK"}},"duplicate":{"title":"Sesija bloķēta","label":"Uzmanību!","text":"Šī lapa jau tika atvērta citur, aizveriet šo cilni."},"finish":{"title":"Sesija noslēgusies","label":"Uzmanību!","text":{"auto":"Sesija beidzās automātiski.","proctor":"Sesiju pārtrauca proktors."},"button":{"ok":"OK"}},"confirm":{"title":"Sesijas pabeigšana","label":"Pabeigt sesiju?","text":"Pēc pabeigšanas jūs nevarēsit turpināt.","checkbox":"Es saprotu un apstiprinu darbību","button":{"ok":"Jā","cancel":"Nē"}},"iframe":{"button":{"home":"Sākumlapa","finish":"Pabeidz","chat":"Tērzēšana","calculator":"Kalkulators","qrcode":"QR kods"}}}'
            ),
          nl: JSON.parse(
            '{"signup":{"title":"Inschrijving voor het evenement","text":"Voer de parameters in van het evenement waaraan je wilt deelnemen. Meestal worden deze parameters geleverd door de organisator van het evenement.","username":"Je login","password":"Je wachtwoord","template":"Identificatiecode van","error":"Opgegeven parameters zijn onjuist","button":{"ok":"OKÉ"}},"wizard":{"title":{"rules":"Regels van het event","check":"Apparatuurcontrole","profile":"Profiel invullen","face":"Een gezichtsfoto maken","passport":"Een identiteitsbewijs uploaden","overview":"Een werkplekoverzicht opnemen","qrcode":"Mobiele camera verbinden"},"button":{"next":"Volgende"},"page":"Stap %{page} van %{total}"},"check":{"text":"Wacht even terwijl het systeem uw computer en het netwerk controleert, zodat mogelijke technische problemen het examen niet verstoren.","empty":"Apparatuurcontrole is niet vereist.","stage":{"browser":"Browser controle","camera":"Webcam controle","microphone":"Microfoon controle","screen":"Scherm controle","network":"Network controle","webrtc":"WebRTC controle"},"button":{"retry":"Probeer opnieuw"},"error":{"Error":" Onbekende fout. Probeer opnieuw.","Unsupported":"Browser wordt niet ondersteund. Probeer uw browser te updaten of gebruik een andere browser.","WrongSize":"Uw browservenster gebruikt niet het volledige scherm. Gebruik het browservenster in fullscreen.","NoRecorder":"MediaRecorder API wordt niet ondersteund of is uitgeschakeld. Schakel deze API in (Settings > Safari > Advanced > Experimental Features > MediaRecorder) of gebruik een andere browser.","NoWindowManagement":"Er is geen toestemming verleend voor toegang tot de modus voor meerdere schermen. Geef toegang tot de plaatsing van het venster op meerdere schermen.","NoPicture":"Geen videobeeld gedetecteerd. Probeer alle andere toepassingen te sluiten en schakel uw antivirusprogrammas uit.","NoVideo":"Webcam is uitgeschakeld of toegang wordt geweigerd. Schakel uw webcam aan en sta de browsertoegang tot de webcam toe.","LowVolume":"Microfoon heeft laag volume of werkt niet. Pas het volume aan of verander uw microfoon.","NoAudio":"Microfoon gedempt of uitgeschakeld. Sluit uw microfoon aan en schakel de browsertoegang tot de microfoon in.","NoCapture":"Geen video van je scherm geregistreerd. Sta browsertoegang tot schermopnames toe.","Multiscreen":"Je hebt niet het hele scherm gedeeld. Schakel de browsertoegang tot het volledige scherm in en ontkoppel eventuele extra schermen.","NoScreen":"De toegang tot uw scherm is uitgeschakeld of een deel van uw scherm is geblokkeerd. Schakel de browsertoegang tot het volledige scherm in.","NoConnection":"WebSocket-verbinding is geblokkeerd. Probeer ad blockers zoals AdBlock of andere vergelijkbare browserextensies uit te schakelen.","RtcError":"Kan geen WebRTC-verbinding tot stand brengen. Probeer uw firewall en antivirus uit te schakelen of maak verbinding met een ander netwerk."}},"profile":{"text":"Vul uw achternaam, voornaam en tweede naam in of controleer deze (indien beschikbaar).","lastname":"Achternaam","firstname":"Voornaam","middlename":"Midden-naam","error":{"unsaved":"Er is een fout opgetreden tijdens het opslaan van gegevens (%{code})"}},"face":{"text":"Maak een foto waarbij uw gezicht in het ovale kader op het scherm past. Zorg ervoor dat er voldoende licht in de kamer is. Als de foto niet is geverifieerd, maak dan een nieuwe foto.","button":{"retry":"Probeer opnieuw","take":"Maak foto"},"msg":{"loading":"<p><b>Bezig met laden...</b></p>","nocamera":"<p><b>Probleem met webcam vastgesteld :(</b></p><p>Probeer hetvolgende:</p><ul><li>Verbind uw camera met de computer</li><li>Sluit alle applicaties van derden die de camera kunnen gebruiken.</li><li>Geef de browser toegang tot uw camera.</li></ul>","noface":"<p><b>Geen gezicht gedetecteerd op de foto :(</b></p><p>Mogelijke oorzaken:</p><ul><li>Je gezicht is buiten beeld.</li><li>Slechte belichting.</li><li>Het gezicht is niet duidelijk zichtbaar door je haar of kleding.</li><li>De camera staat te ver van je af.</li><li>De lichtbron bevindt zich achter je of aan de zijkant.</li></ul><p>Probeer de foto opnieuw te maken.</p>","unverified":"<p><b>Toegang geweigerd :(</b></p><p>Uw foto komt niet overeen met de foto in uw profiel.</p>","done":"<p><b>Foto opgeslagen.</b></p><p>Wanneer u niet tevreden bent met de foto, kunt u de foto opnieuw maken.</p>"}},"passport":{"text":{"photo":"Maak een foto van uw identiteitsbewijs waarop uw foto en naam duidelijk staan.","scan":"Upload een scan van uw identiteitsbewijs waarop uw foto en naam duidelijk staan. Het uploaddocumentformaat is JPEG of PNG.","both":"Maak een foto of upload een scan van uw identiteitsbewijs waarop uw foto en naam duidelijk te zien zijn. Het uploaddocumentformaat is JPEG of PNG."},"textExtra":{"photo":"Maak een foto van de andere bladzijde van uw identiteitsbewijs.","scan":"Upload een scan van een andere pagina van uw identiteitsbewijs. Het formaat van het te uploaden document is JPEG of PNG.","both":"Maak een foto of upload een scan van een andere pagina van uw identiteitsbewijs. Het formaat van het te uploaden document is JPEG of PNG."},"button":{"retry":"Probeer opnieuw","take":"Neem een foto","upload":"Uploaden","add":"+1 foto","reset":"Resetten"},"msg":{"loading":"<p><b>Bezig met laden...</b></p>","ready":"<p><b>Volgende vereisten zijn van toepassing:</b></p><ul><li>Bestandsformaat JPEG of PNG.</li><li>De bestandsgrootte mag niet groter zijn dan 5 MB.</li><li>De beeldresolutie is niet minder dan 1 Mpix.</li><li>Horizontale afbeelding.</li><li>Het document moet één foto bevatten.</li><li>Tekst en foto moeten duidelijk herkenbaar zijn.</li></ul>","nocamera":"<p><b>Probleem met webcam vastgesteld :(</b></p><p>Probeer hetvolgende:</p><ul><li>Verbind uw camera met de computer</li><li>Sluit alle applicaties van derden die de camera kunnen gebruiken.</li><li>Geef de browser toegang tot uw camera.</li></ul>","nophoto":"<p><b>Document is niet gedetecteerd in de afbeelding :(</b></p><p>Mogelijke oorzaken:</p><ul><li>Het document past niet volledig in het frame.</li><li>Het document is niet horizontaal.</li><li>De foto is niet duidelijk in het document.</li><li>De tekst in het document is niet herkenbaar.</li><li>Naam komt niet overeen `%{nickname}`.</li></ul><p>Probeer de foto opnieuw te maken.</p>","noscan":"<p><b>Het document wordt niet gedetecteerd in de scan :(</b></p><p>Mogelijke oorzaken:</p><ul><li>Het bestandsformaat is geen JPEG of PNG.</li><li>De bestandsgrootte is meer dan 5 MB.</li><li>De beeldresolutie is minder dan 1 Mpix.</li><li>Het document is niet horizontaal geörienteerd.</li><li>De foto of tekst in het document is niet duidelijk.</li><li>Naam komt niet overeen `%{nickname}`.</li></ul><p>Probeer een ander bestand te uploaden.</p>","unverified":"<p><b>Toegang geweigerd :(</b></p><p> Het document komt niet overeen met het document in het ledenprofiel.</p>","taken":"<p><b>De foto is opgeslagen.</b></p><p>Wanneer u niet tevreden bent met de foto, kunt u de foto opnieuw maken.</p>","uploaded":"<p><b>Het gescande document is geüpload.</b></p><p>Wanneer u niet tevreden bent met de afbeelding, kunt u het bestand opnieuw uploaden.</p>"}},"overview":{"text":"Neem een korte video op die uw werkruimte laat zien met behulp van uw computercamera of smartphonecamera. Als u een smartphone gebruikt, scan dan de QR-code met uw smartphone en open vervolgens de ontvangen link in de Chrome-browser op Android of Safari op iOS.","expires":"De link is geldig tot %{timeleft}","button":{"retry":"Probeer opnieuw","start":"Begin met opnemen","stop":"Stop met opnemen","save":"Opslaan","qrcode":"QR Code"},"msg":{"loading":"<p><b>Bezig met laden...</b></p>","nocamera":"<p><b>Probleem met webcam vastgesteld :(</b></p><p>Probeer hetvolgende:</p><ul><li>Verbind uw camera met de computer</li><li>Sluit alle applicaties van derden die de camera kunnen gebruiken.</li><li>Geef de browser toegang tot uw camera.</li></ul>","norecord":"<p><b>Probleem met opnemen gedetecteerd :(</b></p><p>Mogelijke redenen:</p><ul><li>Uw camera werkt niet goed</li><li>Uw browser ondersteunt de MediaRecorder API niet</li><li>Er is een probleem met het netwerk</li></ul><p>Probeer het opnieuw of verander uw browser / computer.</p>","done":"<p><b>Video opgeslagen.</b></p><p>U kunt opnieuw opnemen als deze video niet geschikt voor u is.</p>"}},"qrcode":{"text":"Scan de QR-code met uw smartphone en open vervolgens de ontvangen link in de Chrome-browser op Android of Safari op iOS. Sluit uw smartphone aan op de oplader en plaats de camera zo dat wij uw werkplek, u en uw computer kunnen zien.","expires":"De link is geldig tot %{timeleft}"},"ready":{"title":"Gereedheidscontrole","description":"Alles is klaar, nu kun je beginnen met het evenement. Als het evenement niet kan beginnen, probeer het dan later opnieuw of selecteer een ander evenement.","nickname":"Naam","subject":"Titel van het evenement","scheduled":"Geplande tijd","deadline":"Vervaltijd","error":{"ERR_SESSION_NOT_FOUND":"Je hebt geen actieve sessie toegewezen aan je profiel. Je kunt niet verder.","ERR_SEB_INVALID_SIGNATURE":"Dit evenement kan alleen worden uitgevoerd via de Safe Exam Browser, het is niet mogelijk om verder te gaan via uw huidige browser.","ERR_NO_PROCTORS_AVAILABLE":"Er zijn op dit moment geen surveillanten. Probeer het later opnieuw.","ERR_SESSION_TIME_NOT_COME":"Het evenement is nog niet begonnen. Probeer het later opnieuw.","ERR_SESSION_TIME_EXPIRED":"Het evenement is afgelopen, doorgaan is niet mogelijk.","ERR_INVALID_LICENSE":"Ongeldige licentie. U kunt niet verder gaan totdat uw leverancier de licentie heeft verlengd.","ERR_SERVICE_UNAVAILABLE":"De service is tijdelijk niet beschikbaar, probeer het later opnieuw."},"button":{"start":"Begin"}},"chat":{"title":"Chat","inputPlaceholder":"Voer uw bericht in..."},"calculator":{"title":"Calculator"},"conference":{"guest":"Gast","microphone":"Microfoon","camera":"Camera","screen":"Scherm delen","mute":"Geluid aan/uit","single":"Display modes","maximize":"Block size"},"vision":{"qrcode":"Verbind je mobiele camera","events":{"b1":"Browser niet ondersteund","b2":"Focus veranderd naar ander venster","b3":"Full-screen modus uitgeschakelt","c1":"Webcam uitgeschakelt","c2":"Gezicht onzichtbaar of niet gericht op de webcam","c3":"Meerdere gezichten voor de webcam","c4":"Gezicht komt niet overeen met het profiel","c5":"Vergelijkbaar profiel gevonden","k1":"Atypisch toetsenbordhandschrift","m1":"Microfoon gedempt of het volume te laag","m2":"Gesprek of ruis op de achtergrond","n1":"Geen netwerkverbinding","n2":"Geen verbinding met mobiele camera","s1":"Schermactiviteit niet gedeeld","s2":"Tweede display wordt gebruikt"},"button":{"ok":"OK"}},"duplicate":{"title":"Sessie is geblokkeerd","label":"Aandacht!","text":"Deze pagina is ergens anders geopend, sluit dit tabblad."},"finish":{"title":"Sessie voltooid","label":"Aandacht!","text":{"auto":"De sessie is automatisch beëindigd.","proctor":"De sessie werd beëindigd door de proctor."},"button":{"ok":"OK"}},"confirm":{"title":"Sessie afsluiten","label":"De sessie afsluiten?","text":"Eenmaal afgesloten kan u niet meer verdergaan.","checkbox":"Ik begrijp en bevestig de actie","button":{"ok":"Ja","cancel":"Nee"}},"iframe":{"button":{"home":"Homepagina","finish":"Beëindig","chat":"Chatten","calculator":"Rekenmachine","qrcode":"QR code"}}}'
            ),
          pt: JSON.parse(
            '{"signup":{"title":"Inscrições para o evento","text":"Insira os parâmetros do evento do qual você deseja participar. Normalmente, esses parâmetros são fornecidos pelo organizador do evento.","username":"Seu login","password":"Sua senha","template":"Identificador do evento","error":"Os parâmetros específicos estão incorretos","button":{"ok":"OK"}},"wizard":{"title":{"rules":"Regras do evento","check":"Verificação de equipamento","profile":"Preenchendo o perfil","face":"Tirar uma foto de rosto","passport":"Fazer upload de um documento de identidade","overview":"Gravando uma visão geral do local de trabalho","qrcode":"Conexão de câmera móvel"},"button":{"next":"Próximo"},"page":"Passo %{page} de %{total}"},"check":{"text":"Por favor, aguarde enquanto o sistema verifica seu computador e a rede para que possíveis problemas técnicos não interfiram no exame.","empty":" A verificação do equipamento não é necessária.","stage":{"browser":"Verificação do navegador ","camera":"Verificação da webcam","microphone":"Verificação do microfone","screen":"Verificação da tela","network":"Verificação de rede","webrtc":"Verificação WebRTC"},"button":{"retry":"Tentar novamente"},"error":{"Error":" Erro desconhecido. Por favor, tente novamente.","Unsupported":"O navegador ou dispositivo não é compatível. Por favor, use um navegador diferente ou outro dispositivo.","WrongSize":"A janela do seu navegador não está no modo de tela inteira. Por favor, mude para o modo de tela inteira.","NoRecorder":"A API gravação de mídia não é compatível ou está desativada. Por favor, ative esta API (Configurações> Safari> Avançado> Recursos experimentais> Gravação de mídia) ou use um navegador diferente.","NoWindowManagement":"Não foi concedida permissão para acessar o modo de várias telas. Dê acesso ao posicionamento da janela multitela.","NoPicture":"Sem vídeo da câmera. Por favor, tente fechar todos os outros aplicativos e desabilite seu antivírus.","NoVideo":"A webcam está desativada ou não há webcam. Por favor, conecte sua webcam ou habilite o acesso à webcam.","LowVolume":"O volume do microfone está baixo ou não está funcionando. Por favor, ajeite o volume ou altere o microfone.","NoAudio":"Microfone está silenciado ou desativado. Por favor, conecte seu microfone e habilite o acesso do navegador ao microfone.","NoCapture":"Não há nenhum vídeo na sua tela. Por favor, habilite o acesso do navegador à sua tela.","Multiscreen":"Você não compartilhou a tela inteira. Habilite o acesso do navegador a toda a tela e desconecte todos os monitores adicionais.","NoScreen":"O acesso à sua tela está desabilitado ou uma parte da sua tela está bloqueada. Por favor, habilite o acesso do navegador a toda a tela.","NoConnection":"A conexão WebSocket está bloqueada. Por favor, tente desativar o bloqueador de anúncios como AdBlock ou outras extensões de navegador semelhantes.","RtcError":"Não foi possível estabelecer a conexão WebRTC. Por favor, tente desligar o firewall e o antivírus ou conectar-se a uma rede diferente."}},"profile":{"text":"Preencha ou verifique seu sobrenome, nome e nome do meio (se disponível).","lastname":"Último nome","firstname":"Primeiro nome","middlename":"Nome do meio","error":{"unsaved":"Ocorreu um erro ao salvar os dados (%{code})"}},"face":{"text":"Por favor, tire uma foto com o rosto encaixado na moldura oval da tela. Certifique-se de que há luz suficiente na sala. Se a foto não for verificada, tire uma nova foto.","button":{"retry":"Tentar novamente","take":"Tirar uma foto"},"msg":{"loading":"<p><b>Carregando...</b></p>","nocamera":"<p><b>Foi detectado um problema com a webcam :(</b></p><p>Tente o seguinte:</p><ul><li> Conecte sua câmera ao computador </li><li> Feche todos os outros aplicativos que podem usar a câmera. </li><li> Permita o acesso à sua câmera no navegador</li></ul>","noface":"<p><b>Você não foi encontrado na foto :(</b></p><p> Possíveis razões:</p><ul><li>Seu rosto está fora do enquadramento</li><li>Iluminação fraca</li><li>O rosto não está claramente visível devido ao seu cabelo ou roupas</li><li>A câmera está de lado ou muito longe de você</li><li>A fonte de luz está atrás você ou de lado</li></ul><p>Tente tirar a foto novamente.</p>","unverified":"<p><b>Acesso negado :(</b></p><p> Sua foto não coincide com a foto no perfil.</p>","done":"<p><b>Foto salva.</b></p><p>Você pode tirar a foto novamente se não gostar dessa.</p>"}},"passport":{"text":{"photo":"Tire uma foto do seu documento de identidade que mostre claramente sua foto e nome.","scan":"Faça upload de uma digitalização do seu documento de identidade que mostre claramente sua foto e nome. O formato do documento de upload é JPEG ou PNG.","both":"Tire uma foto ou faça upload de uma digitalização de seu documento de identidade que mostre claramente sua foto e nome. O formato do documento de upload é JPEG ou PNG."},"textExtra":{"photo":"Tire uma fotografia da outra página do seu documento de identidade.","scan":"Carregue uma digitalização de outra página do seu documento de identidade. O formato do documento a ser carregado é JPEG ou PNG.","both":"Tire uma fotografia ou carregue uma digitalização de outra página do seu documento de identidade. O formato do documento a ser carregado é JPEG ou PNG."},"button":{"retry":"Tentar novamente","take":"Tirar uma foto","upload":"Fazer upload","add":"+1 foto","reset":"Redefinir"},"msg":{"loading":"<p><b>Carregando...</b></p>","ready":"<p><b>Por favor, siga os requisitos:</b></p><ul><li>Formato de arquivo deve ser JPEG ou PNG</li><li>O tamanho do arquivo não deve exceder 5 MB</li><li>A resolução da imagem não é menor de 1 Mpix</li><li>Arquivo deve ser horizontal</li><li>O documento deve conter uma foto</li><li>O texto e a foto devem ser claramente reconhecíveis</li></ul>","nocamera":"<p><b>Foi detectado um problema com a webcam :(</b></p><p>Por favor, tente o seguinte:</p><ul><li>Conecte a câmera ao seu computador</li><li>Feche todos os outros aplicativos que podem usar a câmera</li><li>Permita o acesso à câmera no navegador</li></ul>","nophoto":"<p><b>O documento não foi detectado na imagem :(</b></p><p>Possíveis razões: </p><ul><li>O documento não se ajusta completamente ao quadro</li><li>O documento não é horizontal</li><li>A foto não está clara no documento</li><li>O texto do documento não é reconhecível</li><li>O nome não corresponde `%{nickname}`</li></ul><p>Por favor, tente tirar a foto novamente.</p>","noscan":"<p><b>O documento não foi detectado na digitalização :(</b></p><p>Possíveis razões:</p><ul><li>O arquivo não está no formato JPEG ou PNG</li><li>Arquivo o tamanho é superior a 5 MB</li><li>A resolução da imagem é inferior a 1 Mpix</li><li>O documento não é horizontal</li><li>A foto ou o texto no documento não está claro</li><li>O nome não corresponde `%{nickname}`</li></ul><p>Por favor, tente enviar um arquivo diferente.</p>","unverified":"<p><b>Acesso negado :(</b></p><p> O documento não corresponde ao documento no perfil do membro.</p>","taken":"<p><b>A foto foi salva.</b></p><p>Se não estiver satisfeito com a foto, você pode tirar a foto novamente.</p>","uploaded":"<p><b>O documento digitalizado foi carregado.</b></p><p>Se não estiver satisfeito com a imagem, você pode carregar o arquivo novamente.</p>"}},"overview":{"text":"Grave um vídeo curto mostrando seu espaço de trabalho usando a câmera do computador ou a câmera do smartphone. Se estiver usando um smartphone, escaneie o código QR usando seu smartphone e abra o link recebido no navegador Chrome no Android ou Safari no iOS.","expires":"O link é válido até %{timeleft}","button":{"retry":"Tentar novamente","start":"Comece a gravar","stop":"Pare de gravar","save":"Salvar","qrcode":"Código QR"},"msg":{"loading":"<p><b>Carregando...</b></p>","nocamera":"<p><b>Foi detectado um problema com a webcam :(</b></p><p>Por favor, tente o seguinte:</p><ul><li>Conecte a câmera ao seu computador</li><li>Feche todos os outros aplicativos que podem usar a câmera</li><li>Permita o acesso à câmera no navegador</li></ul>","norecord":"<p><b>Problema com gravação detectado :(</b></p><p>Razões possíveis:</p><ul><li>Sua câmera não está funcionando corretamente</li><li>Seu navegador não suporta a API MediaRecorder</li><li>Há um problema com a rede</li></ul><p>Por favor, tente novamente ou altere seu navegador / computador.</p>","done":"<p><b>Vídeo salvo.</b></p><p>Você pode regravar se este vídeo não for adequado para você.</p>"}},"qrcode":{"text":"Leia o código QR usando seu smartphone e abra o link recebido no navegador Chrome no Android ou Safari no iOS. Conecte seu smartphone ao carregador e posicione a câmera de forma que possamos ver seu local de trabalho, você e seu computador.","expires":"O link é válido até %{timeleft}"},"ready":{"title":"Verificação de prontidão","description":"Está tudo pronto, agora você pode iniciar o evento. Se o evento não começou, tente novamente mais tarde ou selecione outro evento.","nickname":"Nome","subject":"Título do evento","scheduled":"Horário marcado","deadline":"Data de validade","error":{"ERR_SESSION_NOT_FOUND":"Você não tem nenhuma sessão ativa atribuída ao seu perfil. Você não pode continuar.","ERR_SEB_INVALID_SIGNATURE":"Este evento só pode ser realizado através do Safe Exam Browser, não é possível prosseguir através do seu navegador atual.","ERR_NO_PROCTORS_AVAILABLE":"Não há supervisores disponíveis no momento. Por favor, tente novamente mais tarde.","ERR_SESSION_TIME_NOT_COME":"O evento ainda não começou. Por favor, tente novamente mais tarde.","ERR_SESSION_TIME_EXPIRED":"O evento foi encerrado, não é possível continuar.","ERR_INVALID_LICENSE":"Licença inválida. Você não pode continuar até que seu fornecedor prorrogue a licença.","ERR_SERVICE_UNAVAILABLE":"O serviço está temporariamente indisponível, tente novamente mais tarde."},"button":{"start":"Começar"}},"chat":{"title":"Chat","inputPlaceholder":"Digite sua mensagem..."},"calculator":{"title":"Calculadora"},"conference":{"guest":"Visitante","microphone":"Microfone","camera":"Câmera","screen":"Compartilhamento de tela","mute":"Som ligado/desligado","single":"Modos de exibição","maximize":"Tamanho do bloco"},"vision":{"qrcode":"Conecte sua câmera do celular","events":{"b1":"Navegador não é suportado ","b2":"O foco mudou para uma janela diferente","b3":"Modo de tela inteira desativado","c1":"Webcam desativada","c2":"Rosto invisível ou não olhando para a câmera","c3":"Vários rostos na frente da câmera","c4":"O rosto não corresponde ao perfil","c5":"Foi encontrado um perfil semelhante","k1":"Escrita atípica do teclado","m1":"Microfone foi silenciado ou não está funcionando","m2":"Conversa ou ruído de fundo","n1":"Sem conexão de rede","n2":"Sem conexão com a câmera do celular","s1":"Atividades de tela não compartilhadas","s2":"O segundo display está em uso"},"button":{"ok":"OK"}},"duplicate":{"title":"Sessão está bloqueada","label":"Atenção!","text":"Esta página foi aberta em outro lugar, por favor, feche esta guia."},"finish":{"title":"Sessão concluída","label":"Atenção!","text":{"auto":"A sessão foi encerrada automaticamente.","proctor":"A sessão foi encerrada pelo supervisor."},"button":{"ok":"OK"}},"confirm":{"title":"Conclusão da sessão","label":"Encerrar a sessão?","text":"Ao encerrar a sessão, você não poderá continuar.","checkbox":"Eu entendo e confirmo a ação","button":{"ok":"Sim","cancel":"Não"}},"iframe":{"button":{"home":"Página inicial","finish":"Terminar","chat":"Bater papo","calculator":"Calculadora","qrcode":"Código QR"}}}'
            ),
          ru: JSON.parse(
            '{"signup":{"title":"Регистрация на мероприятие","text":"Введите параметры мероприятия, в котором вы хотите принять участие. Обычно эти параметры предоставляются организатором мероприятия.","username":"Ваш логин","password":"Ваш пароль","template":"Идентификатор мероприятия","error":"Указанные параметры неверны","button":{"ok":"OK"}},"wizard":{"title":{"rules":"Условия проведения мероприятия","check":"Проверка оборудования","profile":"Заполнение профиля","face":"Фотографирование лица","passport":"Загрузка документа","overview":"Запись обзора рабочего места","qrcode":"Подключение мобильной камеры"},"button":{"next":"Далее"},"page":"Шаг %{page} из %{total}"},"check":{"text":"Подождите, пока система проверит компьютер и сеть, чтобы технические проблемы не помешали проведению мероприятия.","empty":"Проверка не требуется.","stage":{"browser":"Проверка браузера","camera":"Проверка веб-камеры","microphone":"Проверка микрофона","screen":"Проверка экрана","network":"Проверка соединения","webrtc":"Проверка WebRTC"},"button":{"retry":"Повторить"},"error":{"Error":"Неизвестная ошибка. Попробуйте повторить проверку снова.","Unsupported":"Ваш браузер или устройство не поддерживается. Попробуйте другой браузер или смените устройство.","WrongSize":"Окно браузера не развернуто на весь экран. Разверните его или перейдите в полноэкранный режим.","NoRecorder":"MediaRecorder API не поддерживается или отключен. Включите этот API (Настройки > Safari > Дополнения > Experimental Features > MediaRecorder) или используйте другой браузер.","NoWindowManagement":"Не дано разрешение на доступ к многоэкранному режиму. Предоставьте доступ к размещению окна в многоэкранном режиме.","NoPicture":"Нет видео с камеры. Попробуйте закрыть все сторонние приложения и отключить антивирус, проверьте работу камеры в браузере.","NoVideo":"Веб-камера не работает или к ней нет доступа. Подключите камеру и разрешите к ней доступ в браузере, проверьте работу камеры в браузере.","LowVolume":"Микрофон неисправен или у него низкая громкость. Настройте громкость микрофона или замените его.","NoAudio":"Микрофон отключен или к нему нет доступа. Подключите микрофон и разрешите к нему доступ в браузере, проверьте работу микрофона в браузере.","NoCapture":"Нет видео с экрана. Не закрывайте доступ к экрану.","Multiscreen":"Не предоставлен доступ ко всему экрану. Отключите дополнительные дисплеи, если есть, и предоставьте доступ ко всему экрану.","NoScreen":"Нет доступа к экрану или доступ предоставлен только к части экрана. Разрешите доступ ко всему экрану.","NoConnection":"Блокируется WebSocket-подключение. Попробуйте отключить блокировщик рекламы AdBlock или аналогичные расширения браузера.","RtcError":"Не удается установить WebRTC подключение. Попробуйте отключить брандмауэр и антивирус или подключитесь к другой сети."}},"profile":{"text":"Введите или проверьте свою фамилию, имя и отчество (если есть).","lastname":"Фамилия","firstname":"Имя","middlename":"Отчество","error":{"unsaved":"Произошла ошибка при сохранении данных (%{code})"}},"face":{"text":"Сфотографируйтесь так, чтобы ваше лицо помещалось в овал на экране. Лицо должно быть равномерно освещено и полностью видно. Если фото не получилось, сделайте новый снимок.","button":{"retry":"Повторить","take":"Сделать снимок"},"msg":{"loading":"<p><b>Загрузка...</b></p>","nocamera":"<p><b>Обнаружена проблема с веб-камерой :(</b></p><p>Попробуйте сделать следующее:</p><ul><li>Подключите камеру к компьютеру</li><li>Закройте все сторонние приложения, которые могут использовать камеру</li><li>Разрешите доступ к камере в браузере</li></ul>","noface":"<p><b>Не нашли вас на фото :(</b></p><p>Возможные причины:</p><ul><li>Лицо не попало в кадр</li><li>Плохое освещение</li><li>Лицо плохо различимо из-за волос или одежды</li><li>Камера находится сбоку или слишком далеко от вас</li><li>Источник света находится позади вас или сбоку</li></ul><p>Попробуйте сфотографироваться еще раз.</p>","unverified":"<p><b>Доступ запрещен :(</b></p><p>Фотография лица не соответствует фотографии в профиле участника.</p>","done":"<p><b>Снимок сохранен.</b></p><p>Если снимок вас не устраивает, то можете сделать снимок повторно.</p>"}},"passport":{"text":{"photo":"Сфотографируйте страницу документа, идентифицирующего/удостоверяющего личность, на которой присутствуют фото и имя участника.","scan":"Загрузите скан одной страницы документа, идентифицирующего/удостоверяющего личность, на которой присутствуют фото и имя участника. Формат загружаемого документа JPEG или PNG.","both":"Сфотографируйте или загрузите скан страницы документа, идентифицирующего/удостоверяющего личность, на которой присутствуют фото и имя участника. Формат загружаемого документа JPEG или PNG."},"textExtra":{"photo":"Сфотографируйте другую страницу документа, идентифицирующего/удостоверяющего личность.","scan":"Загрузите скан другой страницы документа, идентифицирующего/удостоверяющего личность. Формат загружаемого документа JPEG или PNG.","both":"Сфотографируйте или загрузите скан другой страницы документа, идентифицирующего/удостоверяющего личность. Формат загружаемого документа JPEG или PNG."},"button":{"retry":"Повторить","take":"Сделать снимок","upload":"Загрузить","add":"+1 фото","reset":"Сброс"},"msg":{"loading":"<p><b>Загрузка...</b></p>","ready":"<p><b>Соблюдайте следующие требования:</b></p><ul><li>Формат файла JPEG или PNG</li><li>Размер файла не должен превышать 5 МБ</li><li>Разрешение изображения не меньше 1 Мпикс</li><li>Ориентация документа горизонтальная</li><li>Документ должен быть с фотографией</li><li>Фотография должна быть только одна</li><li>Текст и фотография должны находиться на одной странице документа и быть хорошо различимы</li></ul>","nocamera":"<p><b>Обнаружена проблема с веб-камерой :(</b></p><p>Попробуйте сделать следующее:</p><ul><li>Подключите камеру к компьютеру</li><li>Закройте все сторонние приложения, которые могут использовать камеру</li><li>Разрешите доступ к камере в браузере</li></ul>","nophoto":"<p><b>Не обнаружили документ на снимке :(</b></p><p>Возможные причины:</p><ul><li>Документ не полностью помещается в кадр</li><li>Ориентация документа не горизонтальная</li><li>Фото на документе плохо видно</li><li>Текст на документе плохо различим</li><li>ФИО не совпадает с `%{nickname}`</li></ul><p>Попробуйте сделать снимок еще раз.</p>","noscan":"<p><b>Не обнаружили документ на скане :(</b></p><p>Возможные причины:</p><ul><li>Файл не соответствует формату JPEG или PNG</li><li>Размер файла превышает 5 МБ</li><li>Разрешение изображения меньше 1 Мпикс</li><li>Ориентация документа не горизонтальная</li><li>Фото или текст на документе плохо различимы</li><li>ФИО не совпадает с `%{nickname}`</li></ul><p>Попробуйте загрузить другой файл.</p>","unverified":"<p><b>Доступ запрещен :(</b></p><p> Документ не совпадает с документом в профиле участника.</p>","taken":"<p><b>Снимок сохранен.</b></p><p>Если изображение вас не устраивает, то можете сделать снимок повторно.</p>","uploaded":"<p><b>Скан документа загружен.</b></p><p>Если изображение вас не устраивает, то можете загрузить файл повторно.</p>"}},"overview":{"text":"Запишите короткое видео, демонстрирующее ваше рабочее место (включая 360-градусный обзор вашего окружения), используя камеру компьютера или камеру смартфона. В случае использования смартфона отсканируйте QR-код, а затем откройте полученную ссылку в браузере Chrome на Android или в Safari на iOS.","expires":"Ссылка действительна до %{timeleft}","button":{"retry":"Повторить","start":"Начать запись","stop":"Остановить запись","save":"Сохранить","qrcode":"QR-код"},"msg":{"loading":"<p><b>Загрузка...</b></p>","nocamera":"<p><b>Обнаружена проблема с веб-камерой :(</b></p><p>Попробуйте сделать следующее:</p><ul><li>Подключите камеру к компьютеру</li><li>Закройте все сторонние приложения, которые могут использовать камеру</li><li>Разрешите доступ к камере в браузере</li></ul>","norecord":"<p><b>Обнаружена проблема с записью :(</b></p><p>Возможные причины:</p><ul><li>Ваша камера работает некорректно</li><li>Ваш браузер не поддерживает MediaRecorder API</li><li>Возникла проблема с сетью</li></ul><p>Попробуйте еще раз или смените браузер / компьютер.</p>","done":"<p><b>Видео сохранено.</b></p><p>Вы можете перезаписать видео, если оно вас не устраивает.</p>"}},"qrcode":{"text":"Отсканируйте QR-код со смартфона, а затем откройте полученную ссылку в браузере Chrome на Android или в Safari на iOS. Подключите смартфон к зарядному устройству и разместите камеру так, чтобы были видны ваше рабочее место, вы и ваш компьютер.","expires":"Ссылка действительна до %{timeleft}"},"ready":{"title":"Подключение к мероприятию","description":"Все готово, теперь вы можете начать мероприятие. Если начать мероприятие не удалось, то попробуйте повторить попытку позднее или выберите другое мероприятие.","nickname":"Полное имя","subject":"Название мероприятия","scheduled":"Начало входа","deadline":"Окончание входа","error":{"ERR_SESSION_NOT_FOUND":"В данный момент у вас нет ни одного активного сеанса, вы не можете продолжить.","ERR_SEB_INVALID_SIGNATURE":"Данное мероприятие разрешено проходить только через браузер Safe Exam Browser, в этом браузере вы не можете продолжить.","ERR_NO_PROCTORS_AVAILABLE":"В данный момент нет свободных прокторов, повторите попытку позже.","ERR_SESSION_TIME_NOT_COME":"Время вашего мероприятия еще не наступило, повторите попытку позже.","ERR_SESSION_TIME_EXPIRED":"Время вашего мероприятия уже прошло, вы не можете продолжить.","ERR_INVALID_LICENSE":"Недействительная лицензия, вы не можете продолжить пока вендор не продлит лицензию.","ERR_SERVICE_UNAVAILABLE":"Сервис временно недоступен, повторите попытку позже."},"button":{"start":"Начать"}},"chat":{"title":"Чат","inputPlaceholder":"Введите текст сообщения..."},"calculator":{"title":"Калькулятор"},"conference":{"guest":"Гость","microphone":"Микрофон","camera":"Камера","screen":"Демонстрация экрана","mute":"Вкл./выкл. звук","single":"Режимы отображения","maximize":"Размер блока"},"vision":{"qrcode":"Подключите мобильную камеру","events":{"b1":"Браузер не поддерживается","b2":"Переключен фокус на стороннее приложение","b3":"Окно браузера не развернуто на весь экран","c1":"Камера не работает","c2":"Плохо видно лицо перед камерой","c3":"Замечен посторонний человек","c4":"Лицо перед камерой не соответствует профилю","c5":"Обнаружено сходство лица с другим профилем","k1":"Зафиксирован нетипичный клавиатурный почерк","m1":"Микрофон не работает или приглушен","m2":"Слышен разговор или шум на фоне","n1":"Проблема с сетевым подключением","n2":"Проблема с подключением мобильной камеры","s1":"Нет видео с экрана","s2":"Используется дополнительный монитор"},"button":{"ok":"OK"}},"duplicate":{"title":"Сеанс заблокирован","label":"Внимание!","text":"Эта страница была открыта в другом месте, закройте эту вкладку."},"finish":{"title":"Сеанс завершен","label":"Внимание!","text":{"auto":"Сеанс был завершен автоматически.","proctor":"Сеанс был завершен со стороны проктора."},"button":{"ok":"OK"}},"confirm":{"title":"Завершение сеанса","label":"Завершить сеанс?","text":"После завершения вы не сможете продолжить.","checkbox":"Я понимаю и подтверждаю действие","button":{"ok":"Да","cancel":"Нет"}},"iframe":{"button":{"home":"Начальная страница","finish":"Завершить","chat":"Чат","calculator":"Калькулятор","qrcode":"QR-код"}}}'
            ),
          tr: JSON.parse(
            '{"signup":{"title":"Etkinlik için kayıt","text":"Katılmak istediğiniz etkinliğin parametrelerini girin. Genellikle, bu parametreler etkinlik organizatörü tarafından sağlanır.","username":"Giriş bilgileriniz","password":"Şifreniz","template":"Olay tanımlayıcısı","error":"Belirtilen parametreler yanlış","button":{"ok":"TAMAM"}},"wizard":{"title":{"rules":"Etkinliğin kuralları","check":"Ekipman kontrolü","profile":"Profilin doldurulması","face":"Yüz fotoğrafı çekme","passport":"Kimlik belgesi yükleme","overview":"Bir işyerine genel bakış kaydetme","qrcode":"Mobil kamera bağlantısı"},"button":{"next":"Sonraki"},"page":"Adım %{page} / %{total}"},"check":{"text":"Olası teknik sorunların sınavı etkilememesi için lütfen sistem bilgisayarınızı ve ağı kontrol ederken bekleyin.","empty":"Ekipman kontrolü gerekli değildir.","stage":{"browser":"Tarayıcı kontrolü","camera":"Web kamerası kontrolü","microphone":"Mikrofon kontrolü","screen":"Ekran kontrolü","network":"Ağ kontrolü","webrtc":"WebRTC kontrolü"},"button":{"retry":"Tekrar dene"},"error":{"Error":"Bilinmeyen hata. Lütfen tekrar deneyin.","Unsupported":"Tarayıcı veya cihaz desteklenmiyor. Farklı bir tarayıcı veya başka bir cihaz kullanın.","WrongSize":"Tarayıcı pencereniz tam ekran modunda değil. Lütfen tam ekran moduna geçirin.","NoRecorder":"MediaRecorder API desteklenmiyor veya devre dışı. Lütfen bu API\'yi etkinleştirin (Ayarlar > Safari > İleri Düzey > Experimental Features > MediaRecorder) veya farklı bir tarayıcı kullanın.","NoWindowManagement":"Çoklu ekran moduna erişim izni verilmedi. Çoklu ekran pencere yerleşimine erişim verin.","NoPicture":"Kamerada görüntü yok. Diğer tüm uygulamaları kapatmayı ve antivirüs uygulamanızı devre dışı bırakmayı deneyin.","NoVideo":"Web kamerası devre dışı veya web kamerası yok. Web kameranızı bağlayın veya web kamerası erişimini etkinleştirin.","LowVolume":"Mikrofonun sesi düşük veya çalışmıyor. Ses ayarını düzeltin veya mikrofonunuzu değiştirin.","NoAudio":"Mikrofonun sesi kapalı veya devre dışı. Mikrofonunuzu bağlayın ve tarayıcının mikrofona erişimini etkinleştirin.","NoCapture":"Ekranınızdan video yok. Tarayıcının ekranınıza erişimini etkinleştirin.","Multiscreen":"Tüm ekranı paylaşmadınız. Tarayıcının tüm ekrana erişimini etkinleştirin ve ek ekranların bağlantısını kesin.","NoScreen":"Ekranınıza erişim devre dışı veya ekranınızın bir kısmı engellenmiş durumda. Tarayıcının tüm ekrana erişimini etkinleştirin.","NoConnection":"WebSocket bağlantısı engellendi. AdBlock veya benzeri reklam  engelleyiciyi tarayıcı uzantılarını devre dışı bırakmayı deneyin.","RtcError":"WebRTC bağlantısı kurulamıyor. Güvenlik duvarınızı ve antivirüsünüzü kapatmayı veya farklı bir ağa bağlanmayı deneyin."}},"profile":{"text":"Soyadınızı, adınızı ve ikinci adınızı (varsa) doldurun veya kontrol edin.","lastname":"Soyadı","firstname":"İlk adı","middlename":"İkinci ad","error":{"unsaved":"Veriler kaydedilirken bir hata oluştu (%{code})"}},"face":{"text":"Yüzünüzün ekrandaki oval çerçeveye yerleştiği bir fotoğraf çekin. Odada yeterince ışık olduğundan emin olun. Fotoğraf doğrulanmamışsa, lütfen yeni bir fotoğraf çekin.","button":{"retry":"Tekrar dene","take":"Fotoğraf çek"},"msg":{"loading":"<p><b>Yükleniyor...</b></p>","nocamera":"<p><b>Web kamerasıyla ilgili sorun tespit edildi:(</b></p><p>Bunu deneyin:</p><ul><li>Kameranızı bilgisayara bağlayın</li><li>Kamerayı kullanabilen tüm uygulamaları kapatın.</li><li>Tarayıcıdan kameranıza erişime izin verin</li></ul>","noface":"<p><b>Fotoğrafta seni bulamadık:(</b></p><p>Olası nedenler:</p><ul><li>Yüzün çerçevenin dışında</li><li>Zayıf aydınlatma</li><li>Saçınız veya giysileriniz nedeniyle yüzünüz net bir şekilde görünmüyor.</li><li>Kamera yan tarafta veya sizden çok uzakta</li><li>Işık kaynağı arkanızda veya yanınızda</li></ul><p>Fotoğrafı tekrar çekmeyi deneyin.</p>","unverified":"<p><b>Erişim reddedildi :(</b></p><p>Fotoğrafınız üye profilindeki fotoğrafla uyuşmuyor.</p>","done":"<p><b>Anlık görüntü kaydedildi.</b></p><p>Bu fotoğraf uygun değilse yeniden çekebilirsiniz.</p>"}},"passport":{"text":{"photo":"Kimliğinizin, fotoğrafınızı ve adınızı açıkça gösteren bir resmini çekin.","scan":"Fotoğrafınızı ve adınızı açıkça gösteren kimliğinizin taranmış halini yükleyin. Yükleme belgesi formatı JPEG veya PNG\'dir.","both":"Fotoğrafınızı ve adınızı açıkça gösteren bir resim çekin veya kimliğinizin taranmış halini yükleyin. Yükleme belgesi formatı JPEG veya PNG\'dir."},"textExtra":{"photo":"Kimlik belgenizin diğer sayfasının fotoğrafını çekin.","scan":"Kimlik belgenizin başka bir sayfasının taranmış halini yükleyin. Yüklenecek belgenin formatı JPEG veya PNG\'dir.","both":"Bir fotoğraf çekin veya kimlik belgenizin başka bir sayfasının taranmış halini yükleyin. Yüklenecek belgenin formatı JPEG veya PNG\'dir."},"button":{"retry":"Tekrar dene","take":"Fotoğraf çek","upload":"Yükle","add":"+1 fotoğraf","reset":"Sıfırla"},"msg":{"loading":"<p><b>Yükleniyor...</b></p>","ready":"<p><b>Lütfen gereksinimlere uyun:</b></p><ul><li>Dosya biçimi JPEG veya PNG</li><li>Dosya boyutu maksimum 5 MB olmalıdır</li><li>Görüntü çözünürlüğü en az 1 Mpix olmalıdır</li><li>Yatay dosya</li><li>Belge tek fotoğraf içermelidir</li><li>Metin ve fotoğraf açıkça anlaşılır olmalıdır</li></ul>","nocamera":"<p><b>Web kamerasıyla ilgili sorun tespit edildi:(</b></p><p>Lütfen şunları deneyin:</p><ul><li>Kamerayı bilgisayarınıza bağlayın</li><li>Kamerayı kullanabilen tüm uygulamaları kapatın</li><li>Tarayıcının kameraya erişimine izin verin</li></ul>","nophoto":"<p><b>Resimde belge tespit edilemedi:(</b></p><p>Olası nedenler:</p><ul><li>Belge çerçeveye tam olarak sığmıyor</li><li>Belge yatay değil</li><li>Belgedeki fotoğraf net değil</li><li>Belgedeki metin tanınamıyor</li><li>Ad eşleşmiyor `%{nickname}`</li></ul><p>Resmi yeniden çekmeyi deneyin.</p>","noscan":"<p><b>Belge taramada algılanmadı:(</b></p><p>Olası nedenler:</p><ul><li>Dosya JPEG veya PNG formatında değil</li><li>Dosya boyutu 5 MB\'den fazla</li><li>Görüntü çözünürlüğü 1 Mpix\'den az</li><li>Belge yatay değil</li><li>Belgedeki fotoğraf veya metin net değil</li><li>Ad eşleşmiyor `%{nickname}`</li></ul><p>Farklı bir dosya yüklemeyi deneyin.</p>","unverified":"<p><b>Erişim engellendi :(</b></p><p> Belge, üye profilindeki belgeyle eşleşmiyor.</p>","taken":"<p><b>Resim kaydedildi.</b></p><p>Resimden memnun değilseniz, yeniden çekebilirsiniz.</p>","uploaded":"<p><b>Taranan belge yüklendi.</b></p><p>Görüntüden memnun değilseniz, dosyayı tekrar yükleyebilirsiniz.</p>"}},"overview":{"text":"Record a short video showing your workspace using your computer camera or smartphone camera. If using a smartphone, scan the QR code using your smartphone and then open the received link in Chrome browser on Android or Safari on iOS.","expires":"Bağlantı şu süreye boyunca geçerlidir: %{timeleft}","button":{"retry":"Tekrar dene","start":"Kayda başla","stop":"Kaydetmeyi bırak","save":"Kaydetmek","qrcode":"QR kod"},"msg":{"loading":"<p><b>Yükleniyor...</b></p>","nocamera":"<p><b>Web kamerasıyla ilgili sorun tespit edildi:(</b></p><p>Lütfen şunları deneyin:</p><ul><li>Kamerayı bilgisayarınıza bağlayın</li><li>Kamerayı kullanabilen tüm uygulamaları kapatın</li><li>Tarayıcının kameraya erişimine izin verin</li></ul>","norecord":"<p><b>Kayıtla ilgili sorun algılandı :(</b></p><p>Olası nedenler:</p><ul><li>Kameranız düzgün çalışmıyor</li><li>Tarayıcınız MediaRecorder API\'sini desteklemiyor</li><li>Ağda sorun var</li></ul><p>Lütfen tekrar deneyin veya tarayıcınızı / bilgisayarınızı değiştirin.</p>","done":"<p><b>Video kaydedildi.</b></p><p>Bu video size uygun değilse yeniden kaydedebilirsiniz.</p>"}},"qrcode":{"text":"Akıllı telefonunuzu kullanarak QR kodunu tarayın ve ardından alınan bağlantıyı Android\'de Chrome tarayıcısında veya iOS\'ta Safari\'de açın. Akıllı telefonunuzu şarj cihazına bağlayın ve kamerayı iş yerinizi, sizi ve bilgisayarınızı görebileceğimiz şekilde konumlandırın.","expires":"Bağlantı şu süreye boyunca geçerlidir: %{timeleft}"},"ready":{"title":"Hazırlık kontrolü","description":"Her şey hazır, şimdi etkinliğe başlayabilirsiniz. Etkinlik başlayamazsa daha sonra tekrar deneyin veya başka bir etkinlik seçin.","nickname":"Isim","subject":"Olay başlığı","scheduled":"Planlanmış zaman","deadline":"Son kullanma süresi","error":{"ERR_SESSION_NOT_FOUND":"Profilinize atanmış aktif bir oturumunuz yok. Devam edemezsin.","ERR_SEB_INVALID_SIGNATURE":"Bu etkinlik sadece Safe Exam Browser üzerinden gerçekleştirilebilir, mevcut tarayıcınız üzerinden ilerlemeniz mümkün değildir.","ERR_NO_PROCTORS_AVAILABLE":"Şu anda müsait bir gözetmen yok. Lütfen daha sonra tekrar deneyiniz.","ERR_SESSION_TIME_NOT_COME":"Etkinlik henüz başlamadı. Lütfen daha sonra tekrar deneyiniz.","ERR_SESSION_TIME_EXPIRED":"Etkinlik bitmiştir, devamı mümkün değildir.","ERR_INVALID_LICENSE":"Geçersiz lisans. Satıcınız lisansı uzatana kadar devam edemezsiniz.","ERR_SERVICE_UNAVAILABLE":"Hizmet geçici olarak kullanılamıyor, lütfen daha sonra tekrar deneyin."},"button":{"start":"Start"}},"chat":{"title":"Sohbet","inputPlaceholder":"Mesajınızı girin..."},"calculator":{"title":"Hesap Makinası"},"conference":{"guest":"Misafir","microphone":"Mikrofon","camera":"Kamera","screen":"Ekran paylaşımı","mute":"Ses açık/kapalı","single":"Görüntüleme modları","maximize":"Blok boyutu"},"vision":{"qrcode":"Mobil kameranızı bağlayın","events":{"b1":"Tarayıcı desteklenmiyor","b2":"Odak farklı bir pencereye geçti","b3":"Tam ekran modu devre dışı","c1":"Web kamerası devre dışı","c2":"Yüz görünmüyor veya kameraya bakmıyor","c3":"Kameranın önünde birden fazla yüz var","c4":"Yüz profille eşleşmiyor","c5":"Benzer profil bulundu","k1":"Alışılmamış klavye yazısı","m1":"Mikrofonun sesi kapalı veya çalışmıyor","m2":"Konuşma veya arka planda gürültü var","n1":"Ağ bağlantısı yok","n2":"Mobil kameraya bağlantı yok","s1":"Ekran etkinlikleri paylaşılmadı","s2":"İkinci ekran kullanıldı"},"button":{"ok":"TAMAM"}},"duplicate":{"title":"Oturum engellendi","label":"Dikkat!","text":"Bu sayfa başka bir yerde açıldı, bu sekmeyi kapatın."},"finish":{"title":"Oturum tamamlandı","label":"Dikkat!","text":{"auto":"Oturum otomatik olarak sonlandırıldı.","proctor":"Oturum, gözetmen tarafından sonlandırıldı."},"button":{"ok":"TAMAM"}},"confirm":{"title":"Oturumun tamamlanması","label":"Oturum bitirilsin mi?","text":"Tamamlandıktan sonra devam edemezsiniz.","checkbox":"Eylemi anlıyorum ve onaylıyorum","button":{"ok":"Evet","cancel":"Hayır"}},"iframe":{"button":{"home":"Ana sayfa","finish":"Bitir","chat":"Sohbet","calculator":"Hesap makinesi","qrcode":"QR kod"}}}'
            ),
          uk: JSON.parse(
            '{"signup":{"title":"Реєстрація на захід","text":"Введіть параметри заходу, в якому потрібно взяти участь. Зазвичай, ці параметри надаються організатором заходу.","username":"Ваш логін","password":"Ваш пароль","template":"Ідентифікатор заходу","error":"Вказані параметри невірні","button":{"ok":"В ПОРЯДКУ"}},"wizard":{"title":{"rules":"Умови проведення заходу","check":"Перевірка обладнання","profile":"Заповнення профілю","face":"Беручи особа фото","passport":"Завантаження документа, що посвідчує особу","overview":"Запис огляду робочого місця","qrcode":"Підключення мобільної камери"},"button":{"next":"Далі"},"page":"Крок %{page} з %{total}"},"check":{"text":"Зачекайте, поки система перевірить комп\'ютер і мережу, щоб можливі технічні проблеми не завадили заходу.","empty":"Перевірка не потрібно.","stage":{"browser":"Перевірка браузера","camera":"Перевірка веб-камери","microphone":"Перевірка мікрофона","screen":"Перевірка екрану","network":"Перевірка з\'єднання","webrtc":"Перевірка WebRTC"},"button":{"retry":"Повторити"},"error":{"Error":"Невідома помилка. Спробуйте повторити перевірку знову.","Unsupported":"Ваш браузер не підтримується. Спробуйте його оновити або використовуйте інший браузер.","WrongSize":"Вікно браузера не розгорнуто на весь екран. Розгорніть його або перейдіть в повноекранний режим.","NoRecorder":"MediaRecorder API не підтримує або відключений. Увімкніть цей API (Налаштування> Safari> Додатки> Experimental Features> MediaRecorder) або використовуйте інший браузер.","NoWindowManagement":"Не надано дозвіл на доступ до багатоекранного режиму. Надайте доступ до розміщення вікон на кількох екранах.","NoPicture":"Немає відео з камери. Спробуйте закрити всі сторонні додатки і відключити антивірус, перевірте роботу камери в браузері.","NoVideo":"Веб-камера не працює або до неї немає доступу. Підключіть камеру і дозвольте до неї доступ в браузері, перевірте роботу камери в браузері.","LowVolume":"Мікрофон несправний або у нього низька гучність. Налаштуйте гучність мікрофона або замініть його.","NoAudio":"Мікрофон відключений або до нього немає доступу. Підключіть мікрофон і дозвольте до нього доступ в браузері, перевірте роботу мікрофона в браузері.","NoCapture":"Немає відео з екрану. Не закривайте доступ до екрану.","Multiscreen":"Ви не надали доступ до всього екрана. Увімкніть доступ браузера до всього екрана та відключіть усі додаткові дисплеї.","NoScreen":"Неможливо отримати доступ до екрану або доступ надано лише до частини екрану. Дозвольте доступ до всього екрану.","NoConnection":"Блокується WebSocket-підключення. Спробуйте вимкнути функцію блокування реклами AdBlock або аналогічні розширення браузера.","RtcError":"Не вдається встановити WebRTC підключення. Спробуйте відключити брандмауер і антивірус або підключіться до іншої мережі."}},"profile":{"text":"Заповніть або перевірте своє прізвище, ім’я та по батькові (якщо є).","lastname":"Прізвище","firstname":"Ім\'я","middlename":"Середнє ім\'я","error":{"unsaved":"Під час збереження даних сталася помилка (%{code})"}},"face":{"text":"Сфотографуйтеся так, щоб ваше обличчя містилося в овалі на екрані. Обличчя має бути рівномірно освітлене і повністю видне. Якщо фото не вийшло, зробіть нове.","button":{"retry":"Повторити","take":"Зробити знімок"},"msg":{"loading":"<p><b>Завантаження...</b></p>","nocamera":"<p><b>Виявлено проблему з веб-камерою: (</b></p><p>Спробуйте зробити наступне:</p><ul><li>Підключіть камеру до комп\'ютера</li><li>Закрийте всі сторонні додатки, які можуть використовувати камеру</li><li>Дозвольте доступ до камери в браузері</li></ul>","noface":"<p><b>Чи не знайшли вас на фото: (</b></p><p>Можливі причини:</p><ul><li>Особа не потрапила в кадр</li><li>Погане освітлення</li><li>Обличчя погано видно через волосся або одяг</li><li>Камера знаходиться збоку або занадто далеко від вас</li><li>Джерело світла знаходиться позаду вас або збоку</li></ul><p>Спробуйте сфотографуватися ще раз.</p> ","unverified":"<p><b>Доступ заборонений: (</b></p><p>Фотографія особи не відповідає фотографії в профілі учасника.</p>","done":"<p><b>Знімок збережений.</b></p><p>Якщо знімок вас не влаштовує, то можете зробити знімок повторно.</p>"}},"passport":{"text":{"photo":"Сфотографуйте своє посвідчення особи, на якому чітко видно вашу фотографію та ім’я.","scan":"Завантажте скан свого посвідчення особи, на якому чітко видно вашу фотографію та ім’я. Формат документа для завантаження JPEG або PNG.","both":"Сфотографуйте або завантажте скан посвідчення особи, на якому чітко видно вашу фотографію та ім’я. Формат документа для завантаження JPEG або PNG."},"textExtra":{"photo":"Сфотографуйте іншу сторінку свого ідентифікатора.","scan":"Завантажити сканування іншої сторінки вашого ідентифікатора. Формат документа JPEG або PNG, який слід звантажити.","both":"Фотографуйте або завантажуйте сканування іншої сторінки вашого ідентифікатора. Формат документа JPEG або PNG, який слід звантажити."},"button":{"retry":"Повторити","take":"Зробити знімок","upload":"Завантажити","add":"+1 фото","reset":"Скинути"},"msg":{"loading":"<p><b>Завантаження...</b></p>","ready":"<p><b>Будь ласка, дотримуйтесь вимог:</b></p><ul><li>Формат файлу JPEG або PNG</li><li>Розмір файлу не повинен перевищувати 5 МБ</li><li>Роздільна здатність зображення не менше 1 Мпікс</li><li>Горизонтальний файл</li><li>Документ повинен містити одну фотографію</li><li>Текст та фотографії повинні бути чітко впізнаваними</li></ul>","nocamera":"<p><b>Виявлено проблему з веб-камерою :(</b></p><p>Спробуйте наступне:</p><ul><li>Підключіть камеру до комп’ютера</li><li>Закрийте всі сторонні програми, які можуть використовувати камеру</li><li>Дозволити доступ до камери в браузері</li></ul>","nophoto":"<p><b>Документ на зображенні не виявлено :(</b></p><p>Можливі причини:</p><ul><li>Документ не повністю вкладається в рамку</li><li>Документ не є горизонтальним</li><li>Фотографія в документі не чітка</li><li>Текст у документі не розпізнається</li><li>Ім\'я не збігається `%{nickname}`</li></ul><p>Спробуйте зробити знімок ще раз.</p>","noscan":"<p><b>Документ не виявлено при скануванні :(</b></p><p>Можливі причини:</p><ul><li>Файл не має формату JPEG або PNG</li><li>Розмір файлу більше 5 МБ</li><li>Роздільна здатність зображення менше 1 Мпікс</li><li>Документ не є горизонтальним</li><li>Фотографія чи текст у документі незрозумілі</li><li>Ім\'я не збігається `%{nickname}`</li></ul><p>Спробуйте завантажити інший файл.</p>","unverified":"<p><b>Доступ заборонено :(</b></p><p> Документ не збігається з документом у профілі учасника.</p>","taken":"<p><b>Зображення збережено.</b></p><p>Якщо ви незадоволені знімком, ви можете зробити його знову.</p>","uploaded":"<p><b>Сканований документ завантажено.</b></p><p>Якщо зображення незадоволене, ви можете завантажити файл знову.</p>"}},"overview":{"text":"Запишіть коротке відео, яке показує ваше робоче місце, використовуючи камеру комп\'ютера або камеру смартфона. У разі використання смартфона відскануйте QR-код, а потім відкрийте отримане посилання у браузері Chrome на Android або Safari на iOS.","expires":"Посилання дійсне до %{timeleft}","button":{"retry":"Повторити","start":"Почати запис","stop":"Зупинити запис","save":"Зберегти","qrcode":"QR-код"},"msg":{"loading":"<p><b>Завантаження...</b></p>","nocamera":"<p><b>Виявлено проблему з веб-камерою: (</b></p><p>Спробуйте зробити наступне:</p><ul><li>Підключіть камеру до комп\'ютера</li><li>Закрийте всі сторонні додатки, які можуть використовувати камеру</li><li>Дозвольте доступ до камери в браузері</li></ul>","norecord":"<p><b>Виявлено проблему із записом :(</b></p><p>Можливі причини:</p><ul><li>Ваша камера працює некоректно</li><li>Ваш браузер не підтримує MediaRecorder API</li><li>Виникла проблема з мережею</li></ul><p>Спробуйте ще раз або змініть браузер / комп\'ютер.</p>","done":"<p><b>Відео збережено.</b></p><p>Ви можете перезаписати відео, якщо воно вас не влаштовує.</p>"}},"qrcode":{"text":"Відскануйте QR-код за допомогою смартфона, а потім відкрийте отримане посилання у браузері Chrome на Android або Safari на iOS. Підключіть смартфон до зарядного пристрою та розташуйте камеру так, щоб ми могли бачити ваше робоче місце, вас і ваш комп’ютер.","expires":"Посилання дійсне до %{timeleft}"},"ready":{"title":"Перевірка готовності","description":"Все готово, тепер можна приступати до заходу. Якщо подію не вдалося розпочати, спробуйте пізніше або виберіть іншу подію.","nickname":"Ім\'я","subject":"Назва події","scheduled":"Запланований час","deadline":"Час придатності","error":{"ERR_SESSION_NOT_FOUND":"У вашому профілі не призначено жодного активного сеансу, ви не можете продовжувати.","ERR_SEB_INVALID_SIGNATURE":"Цю подію можна здійснити лише через Safe Exam Browser, неможливо продовжити через ваш поточний браузер.","ERR_NO_PROCTORS_AVAILABLE":"На даний момент немає доступних прокторів, спробуйте пізніше.","ERR_SESSION_TIME_NOT_COME":"Подія ще не розпочалася, спробуйте пізніше.","ERR_SESSION_TIME_EXPIRED":"Подія закінчена, продовжити неможливо.","ERR_INVALID_LICENSE":"Недійсна ліцензія. Ви не можете продовжувати, доки ваш постачальник не продовжить ліцензію.","ERR_SERVICE_UNAVAILABLE":"Послуга тимчасово недоступна, спробуйте пізніше."},"button":{"start":"Почніть"}},"chat":{"title":"Чат","inputPlaceholder":"Введіть текст повідомлення..."},"calculator":{"title":"Калькулятор"},"conference":{"guest":"Гість","microphone":"Мікрофон","camera":"Камера","screen":"Демонстрація екрану","mute":"Вкл./Викл. Звук","single":"Режими відображення","maximize":"Розмір блоку"},"vision":{"qrcode":"Підключіть мобільну камеру","events":{"b1":"Браузер не підтримується","b2":"Переключився фокус на сторонній додаток","b3":"Вікно браузера не розгорнуто на весь екран","c1":"Камера не працює","c2":"Погано видно обличчя перед камерою","c3":"Помічена стороння людина","c4":"Особа перед камерою не відповідає профілю","c5":"Виявлено схожість особи з іншим профілем","k1":"Зафіксовано нетиповий клавіатурний почерк","m1":"Мікрофон не працює або приглушений","m2":"Чути розмову або шум на фоні","n1":"Проблема з мережевим підключенням","n2":"Проблема з підключенням мобільної камери","s1":"Немає відео з екрану","s2":"Використовується додатковий монітор"},"button":{"ok":"OK"}},"duplicate":{"title":"Сеанс заблокований","label":"Увага!","text":"Ця сторінка була відкрита в іншому місці, закрийте цю вкладку."},"finish":{"title":"Сеанс завершений","label":"Увага!","text":{"auto":"Сеанс був завершений автоматично.","proctor":"Сеанс був завершений з боку проктора."},"button":{"ok":"OK"}},"confirm":{"title":"Завершення сеансу","label":"Завершити сеанс?","text":"Після завершення ви не зможете продовжити.","checkbox":"Я розумію та підтверджую дію","button":{"ok":"Так","cancel":"Ні"}},"iframe":{"button":{"home":"Початкова сторінка","finish":"Завершити","chat":"Чат","calculator":"Калькулятор","qrcode":"QR-код"}}}'
            ),
          zh: JSON.parse(
            '{"signup":{"title":"活動註冊","text":"輸入您要參加的活動參數。通常，這些參數由活動組織者提供。","username":"您的登入","password":"你的密碼","template":"事件識別碼","error":"指定的參數不正確","button":{"ok":"好"}},"wizard":{"title":{"rules":"事件規則","check":"設備檢查","profile":"填写个人资料","face":"拍照","passport":"上載身分證明文件","overview":"記錄工作場所概覽","qrcode":"手機攝影機連結"},"button":{"next":"下一步"},"page":" 步驟 %{page} 之 %{total}"},"check":{"text":"請稍後，目前系統正在檢查您的設備及網路狀況以免考試中發生技術問題","empty":"檢查不是必要的","stage":{"browser":"瀏覽器檢查","camera":"攝影機檢查","microphone":"麥克風檢查","screen":"螢幕檢查","network":"網路檢查","webrtc":"WebRTC檢查"},"button":{"retry":"再試一次"},"error":{"Error":"不明錯誤，請再試一次","Unsupported":"您的瀏覽器不被支援，請更新或更換瀏覽器","WrongSize":"瀏覽器視窗不是全螢幕模式. 請切換至全螢幕模式.","NoRecorder":"媒體錄製程式介面 API 已被取消或不支援. 請啟用此 API或使用別的瀏覽器.","NoWindowManagement":"未授予访问多屏幕模式的权限。授予访问多屏幕窗口位置的权限。","NoPicture":"攝影機未拍到影片. 請關閉其它應用程式或關閉防毒軟體.","NoVideo":"攝影機被取消或沒有攝影機. 啟用攝影機或連接一台攝影機至電腦","LowVolume":"麥克風音量太低或是無法運作. 調整音量或是更換麥克風.","NoAudio":"麥克風被靜音或是被取消. 連接麥克風並啟用瀏覽器的麥克風功能.","NoCapture":"螢幕中沒有影片. 請啟用瀏覽器的攝影機功能.","Multiscreen":"您尚未共享整个屏幕。启用浏览器访问整个屏幕并拔下任何其他显示器。","NoScreen":"存取螢幕的功能被取消或是部分螢幕被阻擋. 請啟用瀏覽器存取完整螢幕的功能.","NoConnection":"WebSocket 連結被阻擋. 請取消瀏覽器中廣告阻擋程式外掛的功能。例如: AdBlock 或其他類似的外掛.","RtcError":"無法建立WebRTC連接。 嘗試關閉防火牆和防病毒軟件，或連接到其他網絡。"}},"profile":{"text":"填写或检查您的姓氏、名字和中间名（如果有）。","lastname":"姓","firstname":"名","middlename":"中间名字","error":{"unsaved":"保存數據時出錯 (%{code})"}},"face":{"text":"將您的臉貼在螢幕上的橢圓形框內拍照。請確保房間中有足夠的光線，如果照片未通過驗證，請重拍張新照片。","button":{"retry":"再試一次","take":"拍照"},"msg":{"loading":"<p><b>載入中...</b></p>","nocamera":"<p><b>偵測到攝影機問題 :(</b></p><p>請嘗試:</p><ul><li>連接攝影機至電腦</li><li>關閉所有可能使用攝影機的應用程式.</li><li>允許瀏覽器使用攝影機</li></ul>","noface":"<p><b>無法在照片中找到你:(</b></p><p>可能原因:</p><ul><li>臉部超出框架範圍</li><li>光線太暗</li><li>頭髮或衣服遮住臉部</li><li>攝影機未對準您或離您太遠</li><li>光源在您的背後或是偏向旁邊</li></ul><p>請重拍一張照片</p>","unverified":"<p><b>拒絕存取 :(</b></p><p>您的照片不匹配簡歷檔中的照片</p>","done":"<p><b>快照已儲存</b></p><p>如果您覺得此張照片不適合的話，您可以重拍照片</p>"}},"passport":{"text":{"photo":"為您的身份證拍照，清楚地顯示您的照片和姓名。","scan":"上傳您的身份證件掃描件，清楚顯示您的照片和姓名。 上傳文件格式為 JPEG 或 PNG。","both":"拍攝照片或上傳ID掃描件，以清晰顯示您的照片和姓名。 上傳文件格式為 JPEG 或 PNG。"},"textExtra":{"photo":"给你的身份证件的另一页拍照","scan":"上传你的身份文件的另一页的扫描件。要上传的文件的格式是JPEG或PNG。","both":"拍摄一张照片或上传你的身份文件的另一页的扫描件。要上传的文件的格式是JPEG或PNG。"},"button":{"retry":"再試一次","take":"拍攝照片","upload":"上載","add":"+1 張照片","reset":"重启"},"msg":{"loading":"<p><b>載入中...</b></p>","ready":"<p><b>請遵循以下要求：</b></p><ul><li>檔案格式JPEG或PNG</li><li>檔案大小不得超過5 MB</li><li>圖像分辨率不小於1 Mpix</li><li>水平文件</li><li>文件必須包含一張照片</li><li>文字和圖片應清晰可辨</li></ul>","nocamera":"<p><b>檢測到網絡攝像頭的問題:(</b></p><p>請嘗試以下操作：</p><ul><li>將相機連接到計算機</li><li>關閉所有可以使用相機的第三方應用程序</li><li>允許在瀏覽器中訪問相機</li></ul>","nophoto":"<p><b>圖片中未檢測到文件:(</b></p><p>可能的原因：</p><ul><li>文檔未完全適合框架</li><li>文件不是水平的</li><li>照片在文檔中不清晰</li><li>文件中的文字無法識別</li><li>名稱不匹配 `%{nickname}`</li></ul><p>嘗試再次拍攝照片。</p>","noscan":"<p><b>掃描中未檢測到文檔:(</b></p><p>可能的原因：</p><ul><li>該文件不是JPEG或PNG格式</li><li>檔案大小超過5 MB</li><li>圖像分辨率小於1 Mpix</li><li>文件不是水平的</li><li>文檔中的照片或文字不清楚</li><li>名稱不匹配 `%{nickname}`</li></ul><p>嘗試上傳其他文件。</p>","unverified":"<p><b>拒絕訪問 ：（</b></p><p>該文件與會員資料中的文件不匹配。</p>","taken":"<p><b>圖片已保存。</b></p><p>如果對照片不滿意，可以重新拍攝照片。</p>","uploaded":"<p><b>掃描的文檔已上傳。</b></p><p>如果對圖像不滿意，可以再次上傳文件。</p>"}},"overview":{"text":"使用計算機攝像頭或智能手機攝像頭錄製一段短視頻，展示您的工作空間。 如果使用智能手機，請使用智能手機掃描二維碼，然後在 Android 上的 Chrome 瀏覽器或 iOS 上的 Safari 中打開收到的鏈接。","expires":"此連結維持有效至 %{timeleft}","button":{"retry":"再試一次","start":"開始錄製","stop":"停止錄製","save":"節省","qrcode":"二維碼"},"msg":{"loading":"<p><b>載入中...</b></p>","nocamera":"<p><b>偵測到攝影機問題 :(</b></p><p>請嘗試:</p><ul><li>連接攝影機至電腦</li><li>關閉所有可能使用攝影機的應用程式.</li><li>允許瀏覽器使用攝影機</li></ul>","norecord":"<p><b>檢測到錄製問題 :(</b></p><p>可能的原因：</p><ul><li>您的相機無法正常工作</li><li>您的瀏覽器不支持 MediaRecorder API</li><li>網絡有問題</li></ul><p>請重試或更改您的瀏覽器/計算機。</p>","done":"<p><b>視頻已保存。</b></p><p>如果此視頻不適合您，您可以重新錄製。</p>"}},"qrcode":{"text":"使用智能手機掃描二維碼，然後在 Android 上的 Chrome 瀏覽器或 iOS 上的 Safari 中打開收到的鏈接。 將您的智能手機連接到充電器並放置相機，以便我們可以看到您的工作場所、您和您的計算機。","expires":"此連結維持有效至 %{timeleft}"},"ready":{"title":"準備檢查","description":"一切准备就绪，现在您可以开始活动了。如果活动无法开始，请稍后重试或选择其他活动。","nickname":"名稱","subject":"活動標題","scheduled":"計劃的時間","deadline":"到期時間","error":{"ERR_SESSION_NOT_FOUND":"您沒有分配給您的個人資料的任何活動會話。 你不能繼續。","ERR_SEB_INVALID_SIGNATURE":"此事件只能通過 Safe Exam Browser 進行，無法通過您當前的瀏覽器進行。","ERR_NO_PROCTORS_AVAILABLE":"目前沒有可用的監考人員。 請稍後再試。","ERR_SESSION_TIME_NOT_COME":"活動還沒有開始。 請稍後再試。","ERR_SESSION_TIME_EXPIRED":"活動已結束，無法繼續。","ERR_INVALID_LICENSE":"無效的許可證。 在您的供應商延長許可證之前，您無法繼續。","ERR_SERVICE_UNAVAILABLE":"該服務暫時不可用，請稍後重試。"},"button":{"start":"開始"}},"chat":{"title":"聊天","inputPlaceholder":"輸入您的訊息..."},"calculator":{"title":"計算機"},"conference":{"guest":"訪客t","microphone":"麥克風","camera":"攝影機","screen":"分享螢幕","mute":"開/關 聲音","single":"顯示模式","maximize":"區塊大小"},"vision":{"qrcode":"連接手機攝影鏡頭","events":{"b1":"不支援此瀏覽器","b2":"已聚焦至其它視窗","b3":"已取消全螢幕模式","c1":"已取消 Webcam 攝影機","c2":"看不到臉部或沒有直視攝影鏡頭","c3":"數張臉出現在攝影鏡頭前面","c4":"臉部不匹配簡歷檔中資料","c5":"發現一個相同的簡歷","k1":"一個典型的的手寫鍵盤","m1":"麥克風已靜音或音量過低","m2":"背景中有雜音或出現對話","n1":"無網路連結","n2":"無連結至一個手機攝影機","s1":"未分享螢幕畫面","s2":"有使用第二個螢幕"},"button":{"ok":"OK"}},"duplicate":{"title":"監考中斷","label":"注意!","text":"其它地方已開啟此頁，請關閉此頁籤。"},"finish":{"title":"監考完成","label":"注意!","text":{"auto":"會話自動結束。","proctor":"會話由監理員終止。"},"button":{"ok":"OK"}},"confirm":{"title":"會議結束","label":"完成會議？","text":"完成後，您將無法繼續。","checkbox":"我了解並確認該動作","button":{"ok":"是","cancel":"沒有"}},"iframe":{"button":{"home":"主頁","finish":"完","chat":"聊天","calculator":"計算器","qrcode":"二維碼"}}}'
            )
        },
        Ni = Object.keys(ki),
        Ii = Si(),
        Di = !1;
  
      function Ci(e) {
        var t = Si(e);
        return Di = ["he"].indexOf(t) >= 0, Ii = t
      }
  
      function zi() {
        return Ii
      }
  
      function xi() {
        return Di
      }
  
      function Ei(e) {
        var t = arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : {},
          r = function (e, t) {
            if (!t || !e) return e;
            var r = t.split(".");
            return r.reduce((function (e, t) {
              return e ? e[t] : e
            }), e)
          }(ki[Ii], e) || e;
        for (var i in t) r = r.replace("%{".concat(i, "}"), t[i]);
        return r
      }
  
      function Si(e) {
        var t = (e || navigator.language || "en").substring(0, 2);
        return Ni.indexOf(t) < 0 && (t = Ni[0]), t
      }
      const Oi = {
        get active() {
          return !!Ai
        },
        start: () => new Promise((e => {
          if (Ai) return e();
          wi = Ui(), Ai = setInterval((() => {
            wi.parentNode || (wi = Ui())
          }), 1e3), document.addEventListener("contextmenu", Ri), document.addEventListener("keydown",
            Qi), document.addEventListener("keyup", Yi), e()
        })),
        stop: () => new Promise((e => {
          if (!Ai) return e();
          var t;
          clearInterval(Ai), Ai = null, t = wi, (document.head || document.getElementsByTagName("head")[
              0]).removeChild(t), document.removeEventListener("contextmenu", Ri), document
            .removeEventListener("keydown", Qi), document.removeEventListener("keyup", Yi), e()
        }))
      };
  
      function Ri(e) {
        e.preventDefault()
      }
  
      function Qi(e) {
        return 123 === e.keyCode || e.ctrlKey && e.shiftKey && 73 === e.keyCode ? (e.preventDefault(), !1) : !e
          .ctrlKey || 67 !== e.keyCode && 86 !== e.keyCode ? (e.ctrlKey || e.shiftKey) && 45 === e.keyCode || e
          .ctrlKey && 80 === e.keyCode || e.ctrlKey && 83 === e.keyCode || 44 === e.keyCode ? (e
          .preventDefault(), !1) : void 0 : (e.preventDefault(), !1)
      }
  
      function Yi(e) {
        if (44 === e.keyCode) {
          var t = document.createElement("input");
          t.style.position = "fixed", t.style.display = "block", t.style.top = 0, t.style.left = 0, t.style
            .width = "150px", t.style.height = "15px", t.value = "COPYING IS PROHIBITED!", document.body
            .appendChild(t), t.select();
          try {
            document.execCommand("copy")
          } catch (e) {}
          document.body.removeChild(t)
        }
      }
  
      function Ui() {
        var e = document.createElement("style");
        return e.type = "text/css", e.appendChild(document.createTextNode(
          "body { -webkit-user-select: none !important; -moz-user-select: none !important; user-select: none !important; }\n@media print { body { display: none !important; } }\n"
          )), (document.head || document.getElementsByTagName("head")[0]).appendChild(e), e
      }
  
      function Gi(e, t) {
        var r = Object.keys(e);
        if (Object.getOwnPropertySymbols) {
          var i = Object.getOwnPropertySymbols(e);
          t && (i = i.filter((function (t) {
            return Object.getOwnPropertyDescriptor(e, t).enumerable
          }))), r.push.apply(r, i)
        }
        return r
      }
  
      function Bi(e) {
        for (var t = 1; t < arguments.length; t++) {
          var r = null != arguments[t] ? arguments[t] : {};
          t % 2 ? Gi(Object(r), !0).forEach((function (t) {
            Ki(e, t, r[t])
          })) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object
            .getOwnPropertyDescriptors(r)) : Gi(Object(r)).forEach((function (t) {
            Object.defineProperty(e, t, Object.getOwnPropertyDescriptor(r, t))
          }))
        }
        return e
      }
  
      function Ki(e, t, r) {
        return t = function (e) {
          var t = function (e, t) {
            if ("object" != typeof e || null === e) return e;
            var r = e[Symbol.toPrimitive];
            if (void 0 !== r) {
              var i = r.call(e, t || "default");
              if ("object" != typeof i) return i;
              throw new TypeError("@@toPrimitive must return a primitive value.")
            }
            return ("string" === t ? String : Number)(e)
          }(e, "string");
          return "symbol" == typeof t ? t : String(t)
        }(t), t in e ? Object.defineProperty(e, t, {
          value: r,
          enumerable: !0,
          configurable: !0,
          writable: !0
        }) : e[t] = r, e
      }
      var Hi, qi, Wi = [];
      const Vi = {
        get active() {
          return !!Hi
        },
        start: (e, t) => new Promise((r => {
          if (Hi) return r();
          var i, n = Bi(Bi({
              interval: 10,
              timeout: 1e3,
              threshold: 30,
              depth: 100
            }, l.get("tracker.keyboard")), t),
            o = -1,
            a = [],
            s = 0;
          qi = function (e) {
            if (a.push(e), a.length > n.depth)
              if (a.shift(), i) {
                var t = Ji(a, n.timeout);
                o = function (e, t) {
                  var r = 0,
                    i = 3,
                    n = [0, 0, 0],
                    o = [0, 0, 0];
                  for (var a in e)
                    if (t[a]) {
                      for (var s = 0; s < i; s++) n[s] += e[a].mu[s], o[s] += t[a].mu[s];
                      r++
                    } if (!r) return -1;
                  for (var c = 0, l = 0; l < i; l++) n[l] = n[l] / r, o[l] = o[l] / r, c += Math
                    .pow(n[l] - o[l], 2);
                  return c = Math.sqrt(c)
                }(i, t), s > n.depth && o > 0 && o < n.threshold && (! function (e, t) {
                  var r = 3;
                  for (var i in t)
                    if (e[i]) {
                      e[i].count = e[i].count + t[i].count;
                      for (var n = 0; n < r; n++) e[i].mu[n] = (e[i].mu[n] + t[i].mu[n]) / 2
                    } else e[i] = t[i]
                }(i, t), s = 0), s++
              } else i = Ji(a, n.timeout)
          }, Fi(), Hi = setInterval((function () {
            setTimeout(e.bind(null, {
              distance: o,
              threshold: n.threshold,
              verified: o <= n.threshold
            }), 0)
          }), 1e3 * n.interval), r(n)
        })),
        stop: () => new Promise((e => {
          if (!Hi) return e();
          clearInterval(Hi), Hi = null, window.removeEventListener("keydown", Zi), window
            .removeEventListener("keyup", Zi), e()
        }))
      };
  
      function Zi(e) {
        switch ((e = e || window.event).type) {
        case "keydown":
          Wi[e.keyCode] = Date.now();
          break;
        case "keyup":
          if (!Wi[e.keyCode]) break;
          var t = Date.now(),
            r = t - Wi[e.keyCode];
          delete Wi[e.keyCode];
          var i = String.fromCharCode(e.keyCode);
          qi && i.match(/[A-Z]{1}/g) && qi({
            keycode: e.keyCode,
            time: t,
            delta: r
          })
        }
      }
  
      function Fi() {
        window.addEventListener("keydown", Zi), window.addEventListener("keyup", Zi)
      }
  
      function Ji(e) {
        for (var t = arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : 1e3, r = [], i = 0; i < e
          .length - 1; i++) {
          var n = [e[i].keycode, e[i + 1].keycode],
            o = n.join("_");
          r[o] || (r[o] = {
            keycodes: n,
            mu: [0, 0, 0],
            count: 0
          });
          var a = e[i + 1].time - e[i].time;
          a > t || (r[o].count++, r[o].mu[0] += e[i].delta, r[o].mu[1] += e[i + 1].delta, r[o].mu[2] += a)
        }
        for (var s in r)
          if (r[s].count)
            for (var c = 0; c < 3; c++) r[s].mu[c] = r[s].mu[c] / r[s].count;
        return r
      }
  
      function Xi(e, t) {
        var r = Object.keys(e);
        if (Object.getOwnPropertySymbols) {
          var i = Object.getOwnPropertySymbols(e);
          t && (i = i.filter((function (t) {
            return Object.getOwnPropertyDescriptor(e, t).enumerable
          }))), r.push.apply(r, i)
        }
        return r
      }
  
      function _i(e) {
        for (var t = 1; t < arguments.length; t++) {
          var r = null != arguments[t] ? arguments[t] : {};
          t % 2 ? Xi(Object(r), !0).forEach((function (t) {
            $i(e, t, r[t])
          })) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object
            .getOwnPropertyDescriptors(r)) : Xi(Object(r)).forEach((function (t) {
            Object.defineProperty(e, t, Object.getOwnPropertyDescriptor(r, t))
          }))
        }
        return e
      }
  
      function $i(e, t, r) {
        return t = function (e) {
          var t = function (e, t) {
            if ("object" != typeof e || null === e) return e;
            var r = e[Symbol.toPrimitive];
            if (void 0 !== r) {
              var i = r.call(e, t || "default");
              if ("object" != typeof i) return i;
              throw new TypeError("@@toPrimitive must return a primitive value.")
            }
            return ("string" === t ? String : Number)(e)
          }(e, "string");
          return "symbol" == typeof t ? t : String(t)
        }(t), t in e ? Object.defineProperty(e, t, {
          value: r,
          enumerable: !0,
          configurable: !0,
          writable: !0
        }) : e[t] = r, e
      }
      var en, tn, rn, nn = {},
        on = {};
      const an = {
        get active() {
          return !!tn
        },
        start: (e, t) => new Promise(((r, i) => {
          if (tn) return r();
          tn = !0;
          var n = {
            webcam: e,
            screen: t
          };
          rn = Object.keys(n).filter((e => n[e])).map((e => new rr(_i({
            name: e,
            video: n[e],
            duration: 60,
            audioBitsPerSecond: 16384,
            videoBitsPerSecond: 131072
          }, l.get("".concat(e, ".recorder"))))));
          var o = !0,
            a = !0;
          nn = {}, on = {}, Promise.all(sr.hasAddon("track") ? [hr.start((e => {
            sn(nn, on.browser, "b1", !e.supported), sn(nn, on.browser, "b2", !e.focused), sn(
              nn, on.browser, "b3", !e.maximized), u.dispatchEvent("browser", e)
          })).then((e => on.browser = null == e ? void 0 : e.interval)), Lr.start(e, (e => {
            !e || Array.isArray(e) ? (sn(nn, on.camera, "c1", !e), sn(nn, on.camera, "c2",
              e && e.length < 1), sn(nn, on.camera, "c3", e && e.length > 1), sn(nn, on
              .camera, "c4", e && !o), sn(nn, on.camera, "c5", e && !a), u.dispatchEvent(
              "camera", e)) : "object" == typeof e && (o = e.verified, a = !e.similar || !e
              .similar.length, u.dispatchEvent("face", e))
          })).then((e => on.camera = null == e ? void 0 : e.interval)), Er.start(e, (e => {
            sn(nn, on.microphone, "m1", e.muted), sn(nn, on.microphone, "m2", e.voiced), u
              .dispatchEvent("microphone", e)
          })).then((e => on.microphone = null == e ? void 0 : e.interval)), Fr.start((e => {
            sn(nn, on.network, "n1", !e.connected), sn(nn, on.network, "n2", !e.mobile), u
              .dispatchEvent("network", e)
          })).then((e => on.network = null == e ? void 0 : e.interval)), Kr.start(t, (e => {
            sn(nn, on.screen, "s1", !e.captured), sn(nn, on.screen, "s2", !e.natural || !e
              .single), u.dispatchEvent("screen", e)
          })).then((e => on.screen = null == e ? void 0 : e.interval)), Vi.start((e => {
            sn(nn, on.keyboard, "k1", !e.verified), u.dispatchEvent("keyboard", e)
          })).then((e => on.keyboard = null == e ? void 0 : e.interval))] : []).then((() => {
            var e = l.get("tracker.period") || 10,
              t = 0;
            en = setInterval((function () {
              ++t > 60 && (t = 1), t % e == 0 && u.dispatchEvent("metrics", cn(nn, e)), t %
                60 == 0 && ln(nn, rn), sr.hasAddon("record") && rn.forEach((e => e.start()
                  .catch((e => console.warn("Recorder: ".concat(e.message))))))
            }), 1e3), r()
          })).catch(i)
        })),
        stop: () => new Promise(((e, t) => {
          if (!tn) return e();
          tn = !1, clearInterval(en), Promise.all([hr.stop(), Lr.stop(), Er.stop(), Kr.stop(), Vi
          .stop(), Fr.stop()
          ]).then((() => ln(nn, rn))).then(e).catch(t)
        }))
      };
  
      function sn(e, t, r, i) {
        e[r] || (e[r] = []);
        var n = e[r];
        n.push(i ? 1 : -1);
        var o = Math.ceil(60 / (t || 1));
        n.length > o && n.shift()
      }
  
      function cn(e) {
        for (var t, r = arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : 0, i = sr.get(
              "metrics") || [], n = sr.get("weights") || [], o = sr.get("threshold") || 0, a = {}, s = {}, c =
            100, l = 0, d = 0; d < i.length; d++) {
          var u = i[d],
            p = n[d] || 1,
            v = e[u] || [],
            m = Math.ceil(v.length * r / 60),
            h = 0,
            g = (v = v.slice(-m)).length;
          if (g > 0) {
            for (var b = 0, f = 0, y = 0; y < g; y++)(f += v[y]) < 0 && (f = 0), f > b && (b = f);
            h = Math.round(100 * b / g)
          }
          a[u] = h, s[u] = p;
          var M = p * h;
          M > l && (l = M, t = u), c -= M
        }
        return (c = ~~c) < 0 && (c = 0), {
          metrics: a,
          weights: s,
          peak: t,
          score: c,
          threshold: o,
          violated: c < o
        }
      }
  
      function ln(e, t) {
        return Promise.all(t.map((e => e.stop().catch((e => console.warn("Recorder: ".concat(e.message)))))))
          .then((t => {
            var r = t.reduce(((e, t) => (t && e.push(...t), e)), []);
            return u.dispatchEvent("snapshot", _i(_i({}, cn(e)), {}, {
              attach: r
            }))
          }))
      }
      var dn;
      const un = {
        get active() {
          return !!dn
        },
        start() {
          var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {};
          return new Promise((t => {
            if (dn) return t();
            var r = {
                isOpen: !1,
                orientation: void 0
              },
              i = e.threshold || 160;
            dn = setInterval((() => {
              var e = window.devicePixelRatio || 1,
                t = document.documentElement.clientWidth / window.innerWidth,
                n = window.outerWidth - window.innerWidth * e * t > i,
                o = document.documentElement.clientHeight / window.innerHeight,
                a = window.outerHeight - window.innerHeight * e * o > i,
                s = n ? "vertical" : "horizontal";
              n || a ? (r.isOpen && r.orientation === s || u.dispatchEvent("devtools", {
                isOpen: !0,
                orientation: s
              }), r.isOpen = !0, r.orientation = s) : (r.isOpen && u.dispatchEvent("devtools", {
                isOpen: !1
              }), r.isOpen = !1, r.orientation = void 0)
            }), 500), t()
          }))
        },
        stop: () => new Promise((e => {
          if (!dn) return e();
          clearInterval(dn), dn = null, e()
        }))
      };
      class pn {
        constructor(e) {
          this.params = e || {}, this.state = this.data(), this.el = this.render(), this.listen(this.events())
        }
        render() {
          var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : "div";
          return document.createElement(e)
        }
        mount(e) {
          e instanceof HTMLElement && !this.el.parentNode && (e.appendChild(this.el), this.mounted())
        }
        isMounted() {
          return !!this.el.parentNode
        }
        remove() {
          this.el.parentNode && (this.el.remove(), this.removed())
        }
        listen() {
          var e = this,
            t = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {};
          for (var r in t) {
            var i = t[r];
            if ("object" == typeof i) {
              var n = function (t) {
                var n = i[t];
                if ("function" == typeof n) {
                  e.el.addEventListener(r, (r => {
                    var i = e.locate(t, r);
                    i && n(r, i)
                  }), !0)
                }
              };
              for (var o in i) n(o)
            }
          }
        }
        locate(e, t) {
          if (e && t) {
            var r = t.path;
            if (!r) {
              r = [];
              for (var i = t.target; null !== i.parentNode;) r.push(i), i = i.parentNode
            }
            for (var n = 0; n < r.length; n++) {
              var o = r[n];
              if (o instanceof Element == !0 && o.matches(".".concat(e))) return o
            }
          }
        }
        events() {
          return {}
        }
        data() {
          return {}
        }
        getState(e) {
          var t = this.state;
          return e && t ? e.split(".").reduce((function (e, t) {
            return e.value ? {
              value: e.value[t],
              key: t,
              target: e.value
            } : e
          }), {
            value: t
          }) : {}
        }
        setState(e, t) {
          var r = this.state;
          if (!e || !r) return {};
          var i = this.getState(e),
            n = i.value,
            o = i.key,
            a = i.target;
          return void 0 !== t ? a[o] = t : delete a[o], t !== n && this.updated(e, t, n), {
            value: n,
            key: o,
            target: a
          }
        }
        $(e) {
          return (arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : this.el).querySelector("."
            .concat(e))
        }
        $$(e) {
          return (arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : this.el).querySelectorAll(
            ".".concat(e))
        }
        mounted() {}
        updated() {}
        removed() {}
      }
      var vn = r(8512),
        mn = {};
      mn.styleTagTransform = ji(), mn.setAttributes = bi(), mn.insert = hi().bind(null, "head"), mn.domAPI =
      vi(), mn.insertStyleElement = yi();
      ui()(vn.Z, mn);
      const hn = vn.Z && vn.Z.locals ? vn.Z.locals : void 0;
  
      function gn(e, t) {
        var r = Object.keys(e);
        if (Object.getOwnPropertySymbols) {
          var i = Object.getOwnPropertySymbols(e);
          t && (i = i.filter((function (t) {
            return Object.getOwnPropertyDescriptor(e, t).enumerable
          }))), r.push.apply(r, i)
        }
        return r
      }
  
      function bn(e) {
        for (var t = 1; t < arguments.length; t++) {
          var r = null != arguments[t] ? arguments[t] : {};
          t % 2 ? gn(Object(r), !0).forEach((function (t) {
            fn(e, t, r[t])
          })) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object
            .getOwnPropertyDescriptors(r)) : gn(Object(r)).forEach((function (t) {
            Object.defineProperty(e, t, Object.getOwnPropertyDescriptor(r, t))
          }))
        }
        return e
      }
  
      function fn(e, t, r) {
        return t = function (e) {
          var t = function (e, t) {
            if ("object" != typeof e || null === e) return e;
            var r = e[Symbol.toPrimitive];
            if (void 0 !== r) {
              var i = r.call(e, t || "default");
              if ("object" != typeof i) return i;
              throw new TypeError("@@toPrimitive must return a primitive value.")
            }
            return ("string" === t ? String : Number)(e)
          }(e, "string");
          return "symbol" == typeof t ? t : String(t)
        }(t), t in e ? Object.defineProperty(e, t, {
          value: r,
          enumerable: !0,
          configurable: !0,
          writable: !0
        }) : e[t] = r, e
      }
      class yn extends pn {
        constructor() {
          var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {};
          super(e), this._timer = {}, this._video = {
            webcam: e.webcam,
            screen: e.screen
          }, this._p2p = {
            webcam: new er({
              turnURI: l.get("turnURI")
            }),
            screen: new er({
              turnURI: l.get("turnURI")
            }),
            receiver: new er({
              turnURI: l.get("turnURI")
            })
          }, this._p2p.receiver.on("start", (e => {
            var t = e.id,
              r = e.user,
              i = void 0 === r ? "" : r,
              n = e.data,
              o = void 0 === n ? "" : n,
              a = e.stream,
              s = i || ke(),
              c = o || Ei("conference.guest"),
              l = this.appendItem(t, s, {
                footer: [{
                  view: "text",
                  template: c
                }, {
                  view: "button",
                  template: () => '<span class="'.concat(hn.mute_btn, '"></span>'),
                  tooltip: Ei("conference.mute"),
                  click(e) {
                    this.mute(e, this.toggle(e, "muted"))
                  }
                }, {
                  view: "button",
                  template: () => '<span class="'.concat(hn.single_btn, '"></span>'),
                  tooltip: Ei("conference.single"),
                  click(e) {
                    this.toggle(e, "single")
                  }
                }, {
                  view: "button",
                  template: () => '<span class="'.concat(hn.maximize_btn, '"></span>'),
                  tooltip: Ei("conference.maximize"),
                  click(e) {
                    this.maximize(this.toggle(e, "maximized"))
                  }
                }]
              });
            l.srcObject = a, this.mute(t, this.toggle(t, "muted", !1))
          })), this._p2p.receiver.on("stop", (e => {
            var t = e.id;
            this.removeItem(t)
          })), this.mount(e.el || document.body)
        }
        render() {
          return Ci(Re.get("lang")), this.renderLevel1()
        }
        renderCSS(e) {
          if ("string" == typeof e) this.el.classList.add(e);
          else if ("object" == typeof e)
            for (var t in e) this.el.style.setProperty(t, e[t])
        }
        renderLevel1() {
          var e = document.createElement("div");
          return e.className = hn.conference_level1, xi() && e.setAttribute("dir", "rtl"), e
        }
        renderLevel2(e, t) {
          var r = document.createElement("div");
          return r.className = hn.conference_level2, r.dataset.id = e, t && t.appendChild(r), r
        }
        renderLevel3(e, t) {
          var r = t.querySelector("div[data-selected]"),
            i = document.createElement("div");
          return i.className = hn.conference_level3, i.dataset.id = e, r || (i.dataset.selected = !0), t && t
            .appendChild(i), i
        }
        renderFooter(e, t, r) {
          var i = document.createElement("div");
          return i.className = hn.conference_footer, t && t.appendChild(i), (r || []).forEach((t => {
            if (!t.hidden) {
              var r = document.createElement("div");
              r.className = hn["conference_".concat(t.view)], t.template && (r.innerHTML = "function" ==
                typeof t.template ? t.template.call(this, e) : t.template), t.css && (r.className +=
                " ".concat(t.css)), t.tooltip && (r.title = t.tooltip), t.click && (r.onclick = t
                .click.bind(this, e)), i.appendChild(r)
            }
          })), i
        }
        renderVideo(e, t, r) {
          var i = Xt({
              spinner: !0,
              mirror: r
            }),
            n = {
              click: () => {
                this.select(e)
              }
            };
          for (var o in n) i.addEventListener(o, n[o]);
          return t && t.appendChild(i), i
        }
        mount(e) {
          return this.renderCSS(this.params.css), super.mount(e)
        }
        removed() {
          this.stop()
        }
        appendItem(e, t) {
          var r = arguments.length > 2 && void 0 !== arguments[2] ? arguments[2] : {},
            i = this.el,
            n = this.getItem(e);
          n && n.remove();
          var o = i.querySelector('div[data-id="'.concat(t, '"]'));
          o || (o = this.renderLevel2(t, i), r.footer && this.renderFooter(t, o, r.footer));
          var a = this.renderLevel3(e, o),
            s = this.renderVideo(e, a, r.mirror);
          return this.select(e), this.resize(), s
        }
        removeItem(e) {
          var t = this.getItem(e);
          if (t) {
            var r = t.firstChild,
              i = t.parentNode;
            t.remove();
            var n = i.querySelector(".".concat(hn.conference_level3));
            return n ? t.dataset.selected && (n.dataset.selected = !0) : i.remove(), this.resize(), r
          }
        }
        getItem(e) {
          return this.el.querySelector('div[data-id="'.concat(e, '"]'))
        }
        resize() {
          var e = this.el.childElementCount || 1,
            t = window.innerWidth >= window.innerHeight,
            r = Math.sqrt(e),
            i = Math.ceil(r),
            n = Math.round(r),
            o = t ? n : i,
            a = t ? i : n,
            s = this.el;
          s.style.gridTemplateRows = "repeat(".concat(o, ",1fr)"), s.style.gridTemplateColumns = "repeat("
            .concat(a, ",1fr)")
        }
        select(e) {
          var t = this.getItem(e);
          if (t) {
            var r = t.parentNode;
            [].forEach.call(r.querySelectorAll("div[data-selected]"), (e => {
              delete e.dataset.selected
            })), t.dataset.selected = !0
          }
        }
        toggle(e, t, r) {
          var i = this.getItem(e);
          if (i) return r = void 0 !== r ? r : "true" !== i.dataset[t], i.dataset[t] = r, r
        }
        maximize(e) {
          var t = this.el.classList;
          !0 === e ? t.add(hn.expanded) : !1 === e ? t.remove(hn.expanded) : t.toggle(hn.expanded)
        }
        mute(e) {
          var t = !(arguments.length > 1 && void 0 !== arguments[1]) || arguments[1],
            r = this.getItem(e);
          r && [].forEach.call(r.querySelectorAll("video"), (e => {
            e.muted = t
          }))
        }
        audio(e) {
          var t = !(arguments.length > 1 && void 0 !== arguments[1]) || arguments[1],
            r = this.getItem(e);
          r && [].forEach.call(r.querySelectorAll("video"), (e => {
            e.audioEnabled = t
          }))
        }
        video(e) {
          var t = !(arguments.length > 1 && void 0 !== arguments[1]) || arguments[1],
            r = this.getItem(e);
          r && [].forEach.call(r.querySelectorAll("video"), (e => {
            e.videoEnabled = t
          }))
        }
        startWebcam() {
          return new Promise(((e, t) => {
            var r = bn({}, l.get("webcam")),
              i = this._user,
              n = this._video.webcam;
            "object" != typeof n && (n = this.appendItem("webcam", i, {
              mirror: !0,
              footer: [{
                view: "text",
                template: this._name
              }, {
                view: "button",
                template: () => '<span class="'.concat(hn.microphone_btn, '"></span>'),
                tooltip: Ei("conference.microphone"),
                click(e) {
                  this.audio(e, this.toggle(e, "microphone"))
                }
              }, {
                view: "button",
                template: () => '<span class="'.concat(hn.camera_btn, '"></span>'),
                tooltip: Ei("conference.camera"),
                click(e) {
                  this.video(e, this.toggle(e, "camera"))
                }
              }, {
                view: "button",
                hidden: !Jt(),
                template: () => '<span class="'.concat(hn.screen_btn, '"></span>'),
                tooltip: Ei("conference.screen"),
                click(e) {
                  this.toggle(e, "screen") ? this.startScreen() : this.stopScreen()
                }
              }, {
                view: "button",
                template: () => '<span class="'.concat(hn.maximize_btn, '"></span>'),
                tooltip: Ei("conference.maximize"),
                click(e) {
                  this.maximize(this.toggle(e, "maximized"))
                }
              }]
            }), n.muted = !0);
            var o = () => {
              Vt({
                width: r.width,
                height: r.height,
                frameRate: r.frameRate,
                facingMode: "user",
                source: "webcam"
              }).then((t => {
                n.srcObject = t, t.oninactive = () => {
                    this._p2p.webcam.stop(), this.params.restart ? this._timer.webcam =
                      setTimeout(o, 5e3) : this.removeItem("webcam")
                  }, this.mute(i, !0), this.audio(i, this.toggle(i, "microphone", r
                    .audioEnabled)), this.video(i, this.toggle(i, "camera", r.videoEnabled)),
                  this._p2p.webcam.broadcast({
                    stream: t,
                    room: this._room,
                    user: this._user,
                    data: this._name,
                    bitrate: r.bitrate
                  }), e(n)
              })).catch((r => {
                if (n.srcObject) {
                  var i = n.srcObject;
                  i.oninactive = null, i.getTracks().forEach((e => e.stop()))
                }
                if (this.params.restart) return this._timer.webcam = setTimeout(o, 5e3), e(n);
                t(r), console.error(r)
              }))
            };
            o()
          }))
        }
        stopWebcam() {
          return new Promise((e => {
            clearTimeout(this._timer.webcam), this._p2p.webcam.stop(), this.removeItem("webcam"), e()
          }))
        }
        startScreen() {
          return new Promise(((e, t) => {
            var r = bn({}, l.get("screen")),
              i = this._user,
              n = this._video.screen;
            "object" != typeof n && ((n = this.appendItem("screen", i)).muted = !0);
            var o = () => {
              Vt({
                width: r.width,
                height: r.height,
                frameRate: r.frameRate,
                source: "screen"
              }).then((t => {
                n.srcObject = t, t.oninactive = () => {
                  if (this._p2p.screen.stop(), this.params.restart) this._timer.screen =
                    setTimeout(o, 5e3);
                  else {
                    this.removeItem("screen");
                    var e = this.getItem(this._user);
                    e && (e.dataset.screen = !1)
                  }
                }, this._p2p.screen.broadcast({
                  stream: t,
                  room: this._room,
                  user: this._user,
                  data: this._name,
                  bitrate: r.bitrate
                });
                var i = this.getItem(this._user);
                i && (i.dataset.screen = !0), e(n)
              })).catch((r => {
                if (n.srcObject) {
                  var i = n.srcObject;
                  i.oninactive = null, i.getTracks().forEach((e => e.stop()))
                }
                if (this.params.restart) return this._timer.screen = setTimeout(o, 5e3), e(n);
                t(r), console.error(r)
              }))
            };
            o()
          }))
        }
        stopScreen() {
          return new Promise((e => {
            clearTimeout(this._timer.screen), this._p2p.screen.stop(), this.removeItem("screen");
            var t = this.getItem(this._user);
            t && (t.dataset.screen = !1), e()
          }))
        }
        startListener() {
          return new Promise((e => {
            this._p2p.receiver.listen({
              room: this._room,
              user: this._user
            }), e()
          }))
        }
        stopListener() {
          return new Promise((e => {
            this._p2p.receiver.stop(), e()
          }))
        }
        send(e) {
          this._p2p.webcam.send({
            room: this._room,
            user: this._user,
            data: e
          })
        }
        start(e) {
          return this._user = Re.get("id") || ke(), this._name = Re.get("nickname") || Ei("conference.guest"),
            this._room = e || ke(), Promise.all([this._video.webcam && this.startWebcam(), this._video
              .screen && this.startScreen(), this.startListener()
            ]).then((() => {}))
        }
        stop() {
          return Promise.all([this.stopListener(), this._video.screen && this.stopScreen(), this._video
            .webcam && this.stopWebcam()
          ]).then((() => {}))
        }
        restart() {
          var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {},
            t = e.webcam,
            r = e.screen,
            i = [];
          return t && this._video.webcam && i.push(this.stopWebcam().then((() => this.startWebcam()))), r &&
            this._video.screen && i.push(this.stopScreen().then((() => this.startScreen()))), Promise.all(i)
        }
        on(e, t) {
          var r = "".concat(e).split(":"),
            i = r[0],
            n = r[1];
          return this._p2p[i] && this._p2p[i].on(n, t)
        }
        off(e, t) {
          var r = "".concat(e).split(":"),
            i = r[0],
            n = r[1];
          return this._p2p[i] && this._p2p[i].off(n, t)
        }
      }
      var Mn = r(1918),
        jn = {};
      jn.styleTagTransform = ji(), jn.setAttributes = bi(), jn.insert = hi().bind(null, "head"), jn.domAPI =
      vi(), jn.insertStyleElement = yi();
      ui()(Mn.Z, jn);
      const Pn = Mn.Z && Mn.Z.locals ? Mn.Z.locals : void 0;
      var Tn = r(9561),
        Ln = {};
      Ln.styleTagTransform = ji(), Ln.setAttributes = bi(), Ln.insert = hi().bind(null, "head"), Ln.domAPI =
      vi(), Ln.insertStyleElement = yi();
      ui()(Tn.Z, Ln);
      const An = Tn.Z && Tn.Z.locals ? Tn.Z.locals : void 0;
      class wn extends pn {
        constructor(e) {
          super(e);
          var t = e || {},
            r = t.title,
            i = t.close,
            n = t.caption,
            o = t.ok,
            a = t.cancel,
            s = t.disabled;
          this.renderHeader({
            title: r,
            close: i
          }), this.renderBody(), this.renderFooter({
            caption: n,
            ok: o,
            cancel: a,
            disabled: s
          })
        }
        render() {
          var e = document.createElement("DIV");
          return e.className = An.dialog, e.innerHTML = '\n    <div class="'.concat(An.container,
            '">\n      <div class="').concat(An.header, '"></div>\n      <div class="').concat(An.body,
            '"></div>\n      <div class="').concat(An.footer, '"></div>\n    </div>\n    '), e
        }
        events() {
          return {
            click: {
              [An.close_btn]: (e, t) => {
                this.remove();
                var r = this.params.callback;
                "function" == typeof r && r.call(this)
              },
              [An.ok_btn]: (e, t) => {
                if (!this.params.disabled) {
                  var r = this.params.callback;
                  "function" == typeof r && r.call(this, !0)
                }
              },
              [An.cancel_btn]: (e, t) => {
                var r = this.params.callback;
                "function" == typeof r && r.call(this, !1)
              }
            }
          }
        }
        renderHeader(e) {
          var t = e.title,
            r = e.close,
            i = this.$(An.header),
            n = "";
          return t && (n += '<div class="'.concat(An.title, '">').concat(t, "</div>")), r && (n +=
            '<div class="'.concat(An.close_btn, '"></div>')), i.innerHTML = n, i
        }
        renderBody() {
          var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : "",
            t = this.$(An.body);
          return "string" == typeof e ? t.innerHTML = e : (t.innerHTML = "", t.appendChild(e)), t
        }
        renderFooter(e) {
          var t = e.caption,
            r = void 0 === t ? "" : t,
            i = e.ok,
            n = e.cancel,
            o = e.disabled,
            a = this.$(An.footer),
            s = "";
          return (r || i || n) && (s += '<div class="'.concat(An.caption, '">').concat(r, "</div>")), i && (
            s += '<button class="'.concat(An.ok_btn, '" ').concat(o ? "disabled" : "", ">").concat(i,
              "</button>")), n && (s += '<button class="'.concat(An.cancel_btn, '">').concat(n,
            "</button>")), a.innerHTML = s, a
        }
        disable() {
          this.params.disabled = !0;
          var e = this.$(An.ok_btn);
          e && e.setAttribute("disabled", !0)
        }
        enable() {
          this.params.disabled = !1;
          var e = this.$(An.ok_btn);
          e && e.removeAttribute("disabled")
        }
      }
  
      function kn(e, t) {
        var r = Object.keys(e);
        if (Object.getOwnPropertySymbols) {
          var i = Object.getOwnPropertySymbols(e);
          t && (i = i.filter((function (t) {
            return Object.getOwnPropertyDescriptor(e, t).enumerable
          }))), r.push.apply(r, i)
        }
        return r
      }
  
      function Nn(e) {
        for (var t = 1; t < arguments.length; t++) {
          var r = null != arguments[t] ? arguments[t] : {};
          t % 2 ? kn(Object(r), !0).forEach((function (t) {
            In(e, t, r[t])
          })) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object
            .getOwnPropertyDescriptors(r)) : kn(Object(r)).forEach((function (t) {
            Object.defineProperty(e, t, Object.getOwnPropertyDescriptor(r, t))
          }))
        }
        return e
      }
  
      function In(e, t, r) {
        return t = function (e) {
          var t = function (e, t) {
            if ("object" != typeof e || null === e) return e;
            var r = e[Symbol.toPrimitive];
            if (void 0 !== r) {
              var i = r.call(e, t || "default");
              if ("object" != typeof i) return i;
              throw new TypeError("@@toPrimitive must return a primitive value.")
            }
            return ("string" === t ? String : Number)(e)
          }(e, "string");
          return "symbol" == typeof t ? t : String(t)
        }(t), t in e ? Object.defineProperty(e, t, {
          value: r,
          enumerable: !0,
          configurable: !0,
          writable: !0
        }) : e[t] = r, e
      }
      class Dn extends wn {
        constructor() {
          var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {};
          super(Nn(Nn({}, e), {}, {
            callback: t => {
              if (!t) return e.callback();
              this.createSession((() => e.callback(!0)))
            }
          })), this.mount(e.el)
        }
        renderHeader() {
          return super.renderHeader({
            title: Ei("signup.title"),
            close: !0
          })
        }
        renderBody() {
          var e = this.params.payload || {},
            t = Re.get("username") || e.username || "",
            r = e.template || "",
            i = '\n    <div class="'.concat(Pn.signup, '">\n      <div class="').concat(Pn.description,
              '"><div>').concat(Ei("signup.text"), '</div></div>\n      <div class="').concat(Pn.separator,
              '"></div>\n      <div class="').concat(Pn.body, '">\n        <div class="').concat(Pn.row,
              '">\n          <label class="').concat(Pn.label, '">').concat(Ei("signup.username"),
              ' <sup>*</sup></label>\n          <input class="').concat(Pn.value, '" name="username" value="')
            .concat(t, '" ').concat(Re.get("username") ? "disabled" : "",
              '>\n        </div>\n        <div class="').concat(Pn.row, " ").concat(Re.get("username") ? Pn
              .hidden : "", '">\n          <label class="').concat(Pn.label, '">').concat(Ei(
              "signup.password"), '</label>\n          <input class="').concat(Pn.value, " ").concat(Pn
              .password, '" name="password" type="password">\n        </div>\n        <div class="').concat(Pn
              .row, '">\n          <label class="').concat(Pn.label, '">').concat(Ei("signup.template"),
              ' <sup>*</sup></label>\n          <input class="').concat(Pn.value, '" name="template" value="')
            .concat(r, '">\n        </div>\n        <div class="').concat(Pn.row,
              '">\n          <div class="').concat(Pn.message,
              '"></div>\n        </div>\n      </div>\n    </div>\n    ');
          return super.renderBody(i)
        }
        renderFooter() {
          return super.renderFooter({
            ok: Ei("signup.button.ok")
          })
        }
        renderError(e) {
          var t = this.$(Pn.message);
          t.innerHTML = e ? '<span class="'.concat(Pn.text, '">').concat(Ei("signup.error"), "</span>") : ""
        }
        events() {
          return Nn(Nn({}, super.events()), {}, {
            focus: {
              [Pn.password]: (e, t) => {
                t.type = "text"
              }
            },
            blur: {
              [Pn.password]: (e, t) => {
                t.type = "password"
              }
            },
            change: {
              [Pn.value]: () => {
                this.renderError()
              }
            }
          })
        }
        getInputValue(e) {
          return this.el.querySelector('input[name="'.concat(e, '"]')).value || ""
        }
        createSession(e) {
          var t = this.getInputValue("username"),
            r = this.getInputValue("password"),
            i = this.getInputValue("template");
          t && i ? dr.login(Nn(Nn({}, this.params.payload), {}, {
            provider: "signup",
            username: t,
            password: r,
            template: i
          })).then((() => {
            this.remove(), e()
          })).catch((e => {
            this.renderError(e)
          })) : this.renderError(!0)
        }
      }
      var Cn = r(6259),
        zn = {};
      zn.styleTagTransform = ji(), zn.setAttributes = bi(), zn.insert = hi().bind(null, "head"), zn.domAPI =
      vi(), zn.insertStyleElement = yi();
      ui()(Cn.Z, zn);
      const xn = Cn.Z && Cn.Z.locals ? Cn.Z.locals : void 0;
      class En extends pn {
        constructor() {
          var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {};
          super(e), this._messageHandler = this.messageHandler.bind(this), this.mount(e.el)
        }
        render() {
          var e = super.render();
          return e.className = xn.rules, e.innerHTML = '\n    <div class="'.concat(xn.iframe,
            '">\n      <iframe src="').concat(this.state.url,
            '" allow="microphone; camera; autoplay">\n      </iframe>\n    </div>\n    '), e
        }
        mounted() {
          window.addEventListener("message", this._messageHandler, !1);
          var e = this.el.querySelector("iframe");
          e.onerror = e => this.params.onError(e), this.state.url ? e.onload = () => {
            this._timer = setTimeout((() => {
              this.params.onComplete(!0)
            }), 1e3)
          } : this.params.onComplete(!0)
        }
        removed() {
          clearTimeout(this._timer), window.removeEventListener("message", this._messageHandler, !1)
        }
        data() {
          return {
            url: sr.get("rules") || ""
          }
        }
        messageHandler(e) {
          var t = this.el.querySelector("iframe");
          e.source === t.contentWindow && ("WAIT" === e.data && clearTimeout(this._timer), "DONE" === e
            .data && this.params.onComplete(!0), "DENY" === e.data && this.params.onComplete(!1))
        }
      }
      var Sn = r(9461),
        On = {};
      On.styleTagTransform = ji(), On.setAttributes = bi(), On.insert = hi().bind(null, "head"), On.domAPI =
      vi(), On.insertStyleElement = yi();
      ui()(Sn.Z, On);
      const Rn = Sn.Z && Sn.Z.locals ? Sn.Z.locals : void 0;
      class Qn extends pn {
        constructor() {
          var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {};
          super(e), this.mount(e.el)
        }
        render() {
          var e = super.render();
          return e.className = Rn.check, e.innerHTML = '\n    <div class="'.concat(Rn.description, '"><div>')
            .concat(Ei("check.text"), '</div></div>\n    <div class="').concat(Rn.separator,
              '"></div>\n    <div class="').concat(Rn.body, '">').concat(Ei("check.empty"), "</div>\n    "), e
        }
        renderList() {
          var e = this.state.options,
            t = this.state.checks,
            r = this.state.current,
            i = this.state.error;
          return t.map((t => {
            var n = Rn.ready;
            return t === r && (n = i ? Rn.error : Rn.active), e[t] || (n = Rn.passed),
              '\n        <div class="'.concat(Rn.item, '">\n        <div class="').concat(Rn.label,
                '">\n          <span class="').concat(Rn.icon, " ").concat(n,
                '"></span>\n          <span class="').concat(Rn.text, '">').concat(Ei("check.stage."
                .concat(t)), "</span>\n        </div>\n        ").concat(n === Rn.error ? '<div class="'
                .concat(Rn.msg, '">\n          <span>').concat(Ei("check.error.".concat(i.name ||
                  "Error")), '</span>\n          <button class="').concat(Rn.retry_btn, '">').concat(Ei(
                  "check.button.retry"), "</button>\n        </div>") : "", "\n      </div>\n      ")
          })).join("")
        }
        data() {
          var e = sr.get("metrics") || [],
            t = t => e.filter((e => new RegExp("^".concat(t)).test(e))).length > 0,
            r = [],
            i = {};
          return t("b") && (r.push("browser"), i.browser = ri), t("c") && (r.push("camera"), i.camera = ii),
            t("m") && (r.push("microphone"), i.microphone = ni), t("s") && (r.push("screen"), i.screen = oi),
            t("n") && (r.push("network"), i.network = ai), sr.hasAddon("webrtc") && (r.push("webrtc"), i
              .webrtc = si), {
              checks: r,
              options: i,
              current: "",
              error: !1
            }
        }
        events() {
          return {
            click: {
              [Rn.retry_btn]: () => this.checkAll()
            }
          }
        }
        updated() {
          this.$(Rn.body).innerHTML = this.renderList()
        }
        mounted() {
          this.checkAll()
        }
        checkAll() {
          this.setState("error", !1);
          var e = this.state.checks,
            t = r => {
              if (this.isMounted()) {
                this.setState("current", r);
                var i = this.state.options[r];
                return i ? i().then((() => (this.setState("options.".concat(r), null), r = e[e.indexOf(r) +
                  1], t(r)))).catch((e => {
                  this.params.onError(e), this.setState("error", e), console.error(e)
                })) : this.params.onComplete(!0)
              }
            };
          return t(this.state.current || e[0])
        }
      }
      var Yn = r(8497),
        Un = {};
      Un.styleTagTransform = ji(), Un.setAttributes = bi(), Un.insert = hi().bind(null, "head"), Un.domAPI =
      vi(), Un.insertStyleElement = yi();
      ui()(Yn.Z, Un);
      const Gn = Yn.Z && Yn.Z.locals ? Yn.Z.locals : void 0;
      class Bn extends pn {
        constructor() {
          var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {};
          super(e), this.mount(e.el)
        }
        render() {
          var e = (Re.get("nickname") || "").split(/\s+/),
            t = e[0],
            r = e[1],
            i = e[2],
            n = super.render();
          return n.className = Gn.profile, n.innerHTML = '\n    <div class="'.concat(Gn.description,
              '"><div>').concat(Ei("profile.text"), '</div></div>\n    <div class="').concat(Gn.separator,
              '"></div>\n    <div class="').concat(Gn.body, '">\n      <div class="').concat(Gn.row,
              '">\n        <label class="').concat(Gn.label, '">').concat(Ei("profile.lastname"),
              ' <sup>*</sup></label>\n        <input class="').concat(Gn.value, '" name="lastname" value="')
            .concat(t || "", '">\n      </div>\n      <div class="').concat(Gn.row,
              '">\n        <label class="').concat(Gn.label, '">').concat(Ei("profile.firstname"),
              ' <sup>*</sup></label>\n        <input class="').concat(Gn.value, '" name="firstname" value="')
            .concat(r || "", '">\n      </div>\n      <div class="').concat(Gn.row,
              '">\n        <label class="').concat(Gn.label, '">').concat(Ei("profile.middlename"),
              '</label>\n        <input class="').concat(Gn.value, '" name="middlename" value="').concat(i ||
              "", '">\n      </div>\n      <div class="').concat(Gn.row, '">\n        <div class="').concat(Gn
              .message, '"></div>\n      </div>\n    </div>\n    '), n
        }
        renderError(e, t) {
          var r = this.$(Gn.message);
          r.innerHTML = t ? '<span class="'.concat(Gn.text, '">').concat(Ei("profile.error." + e, {
            code: t
          }), "</span>") : ""
        }
        mounted() {
          this.params.onComplete(!0)
        }
        events() {
          return {
            change: {
              [Gn.value]: () => {
                this.saveForm()
              }
            }
          }
        }
        getFormValues() {
          var e = this.el.querySelector('input[name="lastname"]').value || "",
            t = this.el.querySelector('input[name="firstname"]').value || "",
            r = this.el.querySelector('input[name="middlename"]').value || "",
            i = [e, t, r].filter((e => !!e)).join(" ");
          return {
            lastname: e,
            firstname: t,
            middlename: r,
            nickname: i
          }
        }
        saveForm() {
          this.renderError();
          var e = this.getFormValues().nickname;
          return sr.update({
            student: {
              nickname: e
            }
          }).then((t => (Re.get().nickname = e, t))).catch((e => {
            var t = e.code || "500";
            this.renderError("unsaved", t)
          }))
        }
      }
      var Kn = r(8597),
        Hn = {};
      Hn.styleTagTransform = ji(), Hn.setAttributes = bi(), Hn.insert = hi().bind(null, "head"), Hn.domAPI =
      vi(), Hn.insertStyleElement = yi();
      ui()(Kn.Z, Hn);
      const qn = Kn.Z && Kn.Z.locals ? Kn.Z.locals : void 0;
  
      function Wn(e, t) {
        var r = Object.keys(e);
        if (Object.getOwnPropertySymbols) {
          var i = Object.getOwnPropertySymbols(e);
          t && (i = i.filter((function (t) {
            return Object.getOwnPropertyDescriptor(e, t).enumerable
          }))), r.push.apply(r, i)
        }
        return r
      }
  
      function Vn(e, t, r) {
        return t = function (e) {
          var t = function (e, t) {
            if ("object" != typeof e || null === e) return e;
            var r = e[Symbol.toPrimitive];
            if (void 0 !== r) {
              var i = r.call(e, t || "default");
              if ("object" != typeof i) return i;
              throw new TypeError("@@toPrimitive must return a primitive value.")
            }
            return ("string" === t ? String : Number)(e)
          }(e, "string");
          return "symbol" == typeof t ? t : String(t)
        }(t), t in e ? Object.defineProperty(e, t, {
          value: r,
          enumerable: !0,
          configurable: !0,
          writable: !0
        }) : e[t] = r, e
      }
      class Zn extends pn {
        constructor() {
          var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {};
          super(e), this.mount(e.el)
        }
        render() {
          var e = super.render();
          return e.className = qn.face, e.innerHTML = '\n    <div class="'.concat(qn.description,
            '">\n      <div>').concat(Ei("face.text"), '</div>\n    </div>\n    <div class="').concat(qn
            .separator, '"></div>\n    <div class="').concat(qn.body, '">\n      <div class="').concat(qn
            .preview, '">\n        <video class="').concat(qn.webcam,
            '" autoplay playsinline muted data-mirror="true"></video>\n        <div class="').concat(qn
            .overlay, '"></div>\n      </div>\n      <div class="').concat(qn.buttons,
            '">\n        <button class="').concat(qn.take_btn, '">').concat(Ei("face.button.take"),
            '</button>\n        <button class="').concat(qn.retry_btn, " ").concat(qn.hidden, '">').concat(
            Ei("face.button.retry"), "</button>\n      </div>\n    </div>\n    "), e
        }
        events() {
          return {
            click: {
              [qn.take_btn]: (e, t) => {
                t.disabled || this.takePhoto()
              },
              [qn.retry_btn]: (e, t) => {
                t.disabled || this.retry()
              }
            }
          }
        }
        updated(e, t) {
          if ("stage" === e) {
            var r = this.$(qn.overlay),
              i = this.$(qn.take_btn),
              n = this.$(qn.retry_btn);
            switch (i.removeAttribute("disabled"), i.classList.add(qn.hidden), n.classList.add(qn.hidden),
              t) {
            case "ready":
              i.classList.remove(qn.hidden), r.innerHTML = "";
              break;
            case "nocamera":
              n.classList.remove(qn.hidden), r.innerHTML = Ei("face.msg.nocamera");
              break;
            case "noface":
              n.classList.remove(qn.hidden), r.innerHTML = Ei("face.msg.noface");
              break;
            case "nonunique":
              n.classList.remove(qn.hidden), r.innerHTML = Ei("face.msg.nonunique");
              break;
            case "unverified":
              n.classList.remove(qn.hidden), r.innerHTML = Ei("face.msg.unverified");
              break;
            case "loading":
              i.setAttribute("disabled", !0), i.classList.remove(qn.hidden), r.innerHTML = Ei(
                "face.msg.loading");
              break;
            case "done":
              n.classList.remove(qn.hidden), r.innerHTML = Ei("face.msg.done")
            }
          }
        }
        mounted() {
          this.retry(), sr.get("student.face") && this.params.onComplete(!0)
        }
        removed() {
          this._mediaStream && (this._mediaStream.getTracks().forEach((e => e.stop())), delete this
            ._mediaStream), this._url && (URL.revokeObjectURL(this._url), delete this._url)
        }
        retry() {
          this.params.onComplete(!1);
          var e = this.$(qn.webcam);
          this._mediaStream ? (e.play(), this.setState("stage", "ready")) : (this.setState("stage",
            "loading"), delete e.dataset.off, e.dataset.spinner = !0, Vt(function (e) {
              for (var t = 1; t < arguments.length; t++) {
                var r = null != arguments[t] ? arguments[t] : {};
                t % 2 ? Wn(Object(r), !0).forEach((function (t) {
                  Vn(e, t, r[t])
                })) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object
                  .getOwnPropertyDescriptors(r)) : Wn(Object(r)).forEach((function (t) {
                  Object.defineProperty(e, t, Object.getOwnPropertyDescriptor(r, t))
                }))
              }
              return e
            }({
              audio: !1
            }, l.get("webcam"))).then((t => {
              this._mediaStream = t, void 0 !== e.srcObject ? e.srcObject = t : (this._url = URL
                .createObjectURL(t), e.src = this._url), e.play(), e.onplaying = () => {
                delete e.dataset.spinner, this.setState("stage", "ready")
              }
            })).catch((t => {
              this.params.onError(t), delete e.dataset.spinner, e.dataset.off = !0, this.setState(
                "stage", "nocamera")
            })))
        }
        takePhoto() {
          this.setState("stage", "loading");
          var e = this.$(qn.webcam);
          e.paused ? e.play() : Lr.recognize(e, {
            type: "face"
          }).then((t => {
            if (e.pause(), sr.hasAddon("verify") && !1 === t.verified) {
              var r = new Error("Face verification failed");
              return this.setState("stage", "unverified"), void this.params.onError(r)
            }
            return sr.update({
              student: {
                face: t.id
              }
            }).then((() => {
              this.setState("stage", "done"), this.params.onComplete(!0)
            })).catch((e => {
              this.setState("stage", "noface"), this.params.onError(e)
            }))
          })).catch((t => {
            e.pause(), this.setState("stage", "noface"), this.params.onError(t)
          }))
        }
      }
      var Fn = r(1156),
        Jn = {};
      Jn.styleTagTransform = ji(), Jn.setAttributes = bi(), Jn.insert = hi().bind(null, "head"), Jn.domAPI =
      vi(), Jn.insertStyleElement = yi();
      ui()(Fn.Z, Jn);
      const Xn = Fn.Z && Fn.Z.locals ? Fn.Z.locals : void 0;
  
      function _n(e, t) {
        var r = Object.keys(e);
        if (Object.getOwnPropertySymbols) {
          var i = Object.getOwnPropertySymbols(e);
          t && (i = i.filter((function (t) {
            return Object.getOwnPropertyDescriptor(e, t).enumerable
          }))), r.push.apply(r, i)
        }
        return r
      }
  
      function $n(e, t, r) {
        return t = function (e) {
          var t = function (e, t) {
            if ("object" != typeof e || null === e) return e;
            var r = e[Symbol.toPrimitive];
            if (void 0 !== r) {
              var i = r.call(e, t || "default");
              if ("object" != typeof i) return i;
              throw new TypeError("@@toPrimitive must return a primitive value.")
            }
            return ("string" === t ? String : Number)(e)
          }(e, "string");
          return "symbol" == typeof t ? t : String(t)
        }(t), t in e ? Object.defineProperty(e, t, {
          value: r,
          enumerable: !0,
          configurable: !0,
          writable: !0
        }) : e[t] = r, e
      }
      class eo extends pn {
        constructor() {
          var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {};
          super(e), this.mount(e.el)
        }
        render() {
          var e = super.render();
          return e.className = Xn.passport, e.innerHTML = '\n    <div class="'.concat(Xn.description,
              '">\n      <div>').concat(Ei("passport.text." + this.state.mode),
              '</div>\n    </div>\n    <div class="').concat(Xn.separator, '"></div>\n    <div class="')
            .concat(Xn.body, '">\n      <div class="').concat(Xn.preview, '">\n        <video class="')
            .concat(Xn.webcam,
              '" autoplay playsinline muted data-mirror="true"></video>\n        <img class="').concat(Xn
              .image, '" />\n        <div class="').concat(Xn.overlay, '"></div>\n        <div class="')
            .concat(Xn.gallery, '"></div>\n      </div>\n      <div class="').concat(Xn.buttons, " ").concat(
              Xn[this.state.mode], '">\n        <button class="').concat(Xn.take_btn, '">').concat(Ei(
              "passport.button.take"), '</button>\n        <button class="').concat(Xn.upload_btn, '">')
            .concat(Ei("passport.button.upload"), '</button>\n        <button class="').concat(Xn.retry_btn,
              " ").concat(Xn.hidden, '">').concat(Ei("passport.button.retry"),
              '</button>\n        <button class="').concat(Xn.add_btn, " ").concat(Xn.hidden, '">').concat(Ei(
              "passport.button.add"), '</button>\n        <button class="').concat(Xn.reset_btn, " ").concat(
              Xn.hidden, '">').concat(Ei("passport.button.reset"),
              '</button>\n      </div>\n      <input type="file" class="').concat(Xn.file,
              '" accept="image/*" />\n    </div>\n    '), e
        }
        renderOverlay(e) {
          this.$(Xn.overlay).innerHTML = e || ""
        }
        renderGallery(e) {
          var t = this.$(Xn.gallery);
          return t.innerHTML = "", e ? (this.state.images.forEach((e => {
            var r = document.createElement("img");
            r.className = Xn.item, r.dataset.id = e, r.src = "".concat(Ee.url, "/api/storage/")
              .concat(e, "?token=").concat(Ee.token), t.appendChild(r)
          })), t) : t
        }
        reRenderDescription(e) {
          var t = this.$(Xn.description),
            r = Ei("passport.".concat(e, ".").concat(this.state.mode));
          t.innerHTML = "<div>".concat(r, "</div>")
        }
        data() {
          var e = "both";
          return sr.hasAddon("passport") && !sr.hasAddon("scan") ? e = "photo" : sr.hasAddon("scan") && !sr
            .hasAddon("passport") && (e = "scan"), {
              mode: e,
              images: []
            }
        }
        events() {
          return {
            click: {
              [Xn.take_btn]: (e, t) => {
                t.disabled || this.takePhoto()
              },
              [Xn.upload_btn]: (e, t) => {
                t.disabled || this.uploadScan()
              },
              [Xn.retry_btn]: (e, t) => {
                t.disabled || (this.state.images.pop(), this.retry())
              },
              [Xn.add_btn]: (e, t) => {
                t.disabled || (this.reRenderDescription("textExtra"), this.retry())
              },
              [Xn.reset_btn]: (e, t) => {
                t.disabled || (this.state.images = [], this.reRenderDescription("text"), this.saveImages()
                  .then((() => this.retry())))
              }
            }
          }
        }
        updated(e, t) {
          if ("stage" === e) {
            var r = this.$(Xn.take_btn),
              i = this.$(Xn.upload_btn),
              n = this.$(Xn.retry_btn),
              o = this.$(Xn.add_btn),
              a = this.$(Xn.reset_btn);
            r.removeAttribute("disabled"), i.removeAttribute("disabled"), r.classList.add(Xn.hidden), i
              .classList.add(Xn.hidden), n.classList.add(Xn.hidden), o.classList.add(Xn.hidden), a.classList
              .add(Xn.hidden), this.renderOverlay(), this.renderGallery();
            var s = parseInt(l.get("passport.maxPages")) || 2,
              c = this.state.images.length;
            switch (t) {
            case "ready":
              r.classList.remove(Xn.hidden), i.classList.remove(Xn.hidden), this.renderOverlay("scan" === this
                .state.mode ? Ei("passport.msg.ready") : "");
              break;
            case "nocamera":
              n.classList.remove(Xn.hidden), this.renderOverlay(Ei("passport.msg.nocamera"));
              break;
            case "nophoto":
              n.classList.remove(Xn.hidden), this.renderOverlay(Ei("passport.msg.nophoto", {
                nickname: Re.get("nickname")
              }));
              break;
            case "noscan":
              n.classList.remove(Xn.hidden), this.renderOverlay(Ei("passport.msg.noscan", {
                nickname: Re.get("nickname")
              }));
              break;
            case "unverified":
              n.classList.remove(Xn.hidden), this.renderOverlay(Ei("passport.msg.unverified"));
              break;
            case "loading":
              r.setAttribute("disabled", !0), i.setAttribute("disabled", !0), r.classList.remove(Xn.hidden), i
                .classList.remove(Xn.hidden), this.renderOverlay(Ei("passport.msg.loading"));
              break;
            case "taken":
              n.classList.remove(Xn.hidden), this.renderOverlay(Ei("passport.msg.taken")), sr.hasAddon(
                  "extrapages") && c < s ? (o.classList.remove(Xn.hidden), c > 1 && this.renderGallery(!0)) :
                c === s && (a.classList.remove(Xn.hidden), this.renderGallery(!0));
              break;
            case "uploaded":
              n.classList.remove(Xn.hidden), this.renderOverlay(Ei("passport.msg.uploaded")), sr.hasAddon(
                  "extrapages") && c < s ? (o.classList.remove(Xn.hidden), c > 1 && this.renderGallery(!0)) :
                c === s && (a.classList.remove(Xn.hidden), this.renderGallery(!0))
            }
          }
        }
        mounted() {
          this.retry(), sr.get("student.passport") && this.params.onComplete(!0)
        }
        removed() {
          this._mediaStream && (this._mediaStream.getTracks().forEach((e => e.stop())), delete this
            ._mediaStream), this._url && (URL.revokeObjectURL(this._url), delete this._url)
        }
        retry() {
          this.params.onComplete(!1);
          var e = this.$(Xn.webcam),
            t = this.$(Xn.image);
          sr.hasAddon("passport") ? (e.classList.remove(Xn.hidden), t.classList.add(Xn.hidden), this
            ._mediaStream ? (e.play(), this.setState("stage", "ready")) : (this.setState("stage",
              "loading"), delete e.dataset.off, e.dataset.spinner = !0, Vt(function (e) {
                for (var t = 1; t < arguments.length; t++) {
                  var r = null != arguments[t] ? arguments[t] : {};
                  t % 2 ? _n(Object(r), !0).forEach((function (t) {
                    $n(e, t, r[t])
                  })) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object
                    .getOwnPropertyDescriptors(r)) : _n(Object(r)).forEach((function (t) {
                    Object.defineProperty(e, t, Object.getOwnPropertyDescriptor(r, t))
                  }))
                }
                return e
              }({
                audio: !1
              }, l.get("webcam"))).then((t => {
                this._mediaStream = t, void 0 !== e.srcObject ? e.srcObject = t : (this._url = URL
                  .createObjectURL(t), e.src = this._url), e.play(), e.onplaying = () => {
                  delete e.dataset.spinner, this.setState("stage", "ready")
                }
              })).catch((t => {
                this.params.onError(t), delete e.dataset.spinner, e.dataset.off = !0, this.setState(
                  "stage", "nocamera")
              })))) : (e.classList.add(Xn.hidden), t.classList.remove(Xn.hidden), t && t.removeAttribute(
            "src"), this._url && (URL.revokeObjectURL(this._url), delete this._url), this.setState(
            "stage", "ready"))
        }
        takePhoto() {
          this.setState("stage", "loading");
          var e = this.$(Xn.webcam);
          if (e.classList.remove(Xn.hidden), this.$(Xn.image).classList.add(Xn.hidden), e.paused) e.play();
          else {
            var t = this.state.images;
            Lr.recognize(e, {
              type: t.length > 0 ? "extrapages" : "passport"
            }).then((r => {
              if (e.pause(), !t.length && sr.hasAddon("verify") && !1 === r.verified) {
                var i = new Error("Passport verification failed");
                return this.setState("stage", "unverified"), void this.params.onError(i)
              }
              return t.push(r.id), this.saveImages().then((() => {
                this.setState("stage", "taken")
              })).catch((e => {
                t.pop(), this.setState("stage", "nophoto"), this.params.onError(e)
              }))
            })).catch((t => {
              e.pause(), this.setState("stage", "nophoto"), this.params.onError(t)
            }))
          }
        }
        uploadScan() {
          var e = this.$(Xn.file);
          e.onchange = null, e.value = null, e.onchange = e => {
            this.setState("stage", "loading");
            var t = e.target.files[0];
            if (!t || !/^image\//.test(t.type)) {
              var r = new Error("The uploaded file is not an image");
              return this.setState("stage", "noscan"), void this.params.onError(r)
            }
            var i = this.$(Xn.webcam);
            i.classList.add(Xn.hidden);
            var n = this.$(Xn.image);
            n.classList.remove(Xn.hidden), n.onload = () => {
              var e = n.naturalWidth,
                t = n.naturalHeight,
                r = 1 / (e + t) * 1917,
                o = e * r,
                a = t * r,
                s = this.state.images;
              Lr.recognize(n, {
                type: s.length > 0 ? "extrapages" : "passport",
                width: o,
                height: a
              }).then((e => {
                if (!s.length && sr.hasAddon("verify") && !1 === e.verified) {
                  var t = new Error("Passport verification failed");
                  return this.setState("stage", "unverified"), void this.params.onError(t)
                }
                return s.push(e.id), this.saveImages().then((() => {
                  this.setState("stage", "uploaded")
                })).catch((e => {
                  s.pop(), this.setState("stage", "noscan"), this.params.onError(e)
                }))
              })).catch((e => {
                i.pause(), this.setState("stage", "noscan"), this.params.onError(e)
              }))
            }, this._url = URL.createObjectURL(t), n.src = this._url
          }, e.click()
        }
        saveImages() {
          var e = this.state.images;
          return sr.update({
            student: {
              passport: e[0],
              extrapages: e.slice(1)
            }
          }).then((t => {
            var r = l.get("passport.maxPages") || 2;
            return (!sr.hasAddon("extrapages") || sr.hasAddon("extrapages") && e.length >= r) && this
              .params.onComplete(!0), t
          }))
        }
      }
      var to = r(4123),
        ro = {};
      ro.styleTagTransform = ji(), ro.setAttributes = bi(), ro.insert = hi().bind(null, "head"), ro.domAPI =
      vi(), ro.insertStyleElement = yi();
      ui()(to.Z, ro);
      const io = to.Z && to.Z.locals ? to.Z.locals : void 0;
  
      function no(e, t) {
        var r = Object.keys(e);
        if (Object.getOwnPropertySymbols) {
          var i = Object.getOwnPropertySymbols(e);
          t && (i = i.filter((function (t) {
            return Object.getOwnPropertyDescriptor(e, t).enumerable
          }))), r.push.apply(r, i)
        }
        return r
      }
  
      function oo(e) {
        for (var t = 1; t < arguments.length; t++) {
          var r = null != arguments[t] ? arguments[t] : {};
          t % 2 ? no(Object(r), !0).forEach((function (t) {
            ao(e, t, r[t])
          })) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object
            .getOwnPropertyDescriptors(r)) : no(Object(r)).forEach((function (t) {
            Object.defineProperty(e, t, Object.getOwnPropertyDescriptor(r, t))
          }))
        }
        return e
      }
  
      function ao(e, t, r) {
        return t = function (e) {
          var t = function (e, t) {
            if ("object" != typeof e || null === e) return e;
            var r = e[Symbol.toPrimitive];
            if (void 0 !== r) {
              var i = r.call(e, t || "default");
              if ("object" != typeof i) return i;
              throw new TypeError("@@toPrimitive must return a primitive value.")
            }
            return ("string" === t ? String : Number)(e)
          }(e, "string");
          return "symbol" == typeof t ? t : String(t)
        }(t), t in e ? Object.defineProperty(e, t, {
          value: r,
          enumerable: !0,
          configurable: !0,
          writable: !0
        }) : e[t] = r, e
      }
      class so extends pn {
        constructor() {
          var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {};
          super(e), this._eventHandler = t => {
            t && "mobile" === t.event && e.onComplete.call(this, !0)
          }, this.mount(e.el)
        }
        render() {
          var e = super.render();
          return e.className = io.overview, e.innerHTML = '\n    <div class="'.concat(io.description,
              '">\n      <div>').concat(Ei("overview.text"), '</div>\n    </div>\n    <div class="').concat(io
              .separator, '"></div>\n    <div class="').concat(io.body, '">\n      <div class="').concat(io
              .recording, '">\n        <div class="').concat(io.preview, '">\n          <video class="')
            .concat(io.webcam,
              '"\n            loop autoplay playsinline muted disablepictureinpicture\n            controlslist="nodownload nofullscreen noremoteplayback">\n          </video>\n          <div class="'
              ).concat(io.overlay, '"></div>\n          <div class="').concat(io.timer,
              '"></div>\n        </div>\n        <div class="').concat(io.buttons,
              '">\n          <button class="').concat(io.action_btn, '">').concat(Ei("overview.button.start"),
              '</button>\n          <button class="').concat(io.qrcode_btn, '">').concat(Ei(
              "overview.button.qrcode"), '</button>\n          <button class="').concat(io.retry_btn, " ")
            .concat(io.hidden, '">').concat(Ei("overview.button.retry"),
              '</button>\n        </div>\n      </div>\n      <img class="').concat(io.qrcode, " ").concat(io
              .hidden, '" />\n    </div>\n    '), e
        }
        renderTimer(e) {
          var t = this.$(io.timer),
            r = new Date(1e3 * e).toJSON().slice(14, 19);
          t.innerHTML = e ? "&#9898; ".concat(r) : ""
        }
        events() {
          return {
            click: {
              [io.action_btn]: (e, t) => {
                t.disabled || this.start()
              },
              [io.qrcode_btn]: (e, t) => {
                t.disabled || this.qrcode()
              },
              [io.retry_btn]: (e, t) => {
                t.disabled || this.retry()
              },
              [io.qrcode]: (e, t) => {
                this.qrcode()
              }
            }
          }
        }
        updated(e, t) {
          if ("stage" === e) {
            var r = this.$(io.overlay),
              i = this.$(io.action_btn),
              n = this.$(io.qrcode_btn),
              o = this.$(io.retry_btn);
            switch (i.removeAttribute("disabled"), i.classList.add(io.hidden), n.classList.add(io.hidden), o
              .classList.add(io.hidden), t) {
            case "ready":
              n.classList.remove(io.hidden), i.classList.remove(io.hidden), i.innerHTML = Ei(
                "overview.button.start"), r.innerHTML = "";
              break;
            case "loading":
              i.setAttribute("disabled", !0), i.classList.remove(io.hidden), r.innerHTML = Ei(
                "overview.msg.loading");
              break;
            case "recording":
              i.classList.remove(io.hidden), i.innerHTML = Ei("overview.button.stop"), r.innerHTML = "";
              break;
            case "recorded":
              i.classList.remove(io.hidden), o.classList.remove(io.hidden), i.innerHTML = Ei(
                "overview.button.save"), r.innerHTML = "";
              break;
            case "done":
              o.classList.remove(io.hidden), r.innerHTML = Ei("overview.msg.done");
              break;
            case "nocamera":
              o.classList.remove(io.hidden), r.innerHTML = Ei("overview.msg.nocamera");
              break;
            case "norecord":
              o.classList.remove(io.hidden), r.innerHTML = Ei("overview.msg.norecord")
            }
          } else if ("qrcode" === e) {
            var a = this.$(io.qrcode);
            a.src = t.qrcode, a.title = Ei("overview.expires", {
              timeleft: new Date(1e3 * t.exp).toLocaleString(zi())
            })
          }
        }
        mounted() {
          Ke.on("userdata", this._eventHandler), this.retry(), sr.get("overview") && this.params.onComplete(!
            0)
        }
        removed() {
          Ke.off("userdata", this._eventHandler), delete this._eventHandler, delete this._file, delete this
            ._recorder, this._mediaStream && (this._mediaStream.getTracks().forEach((e => e.stop())),
              delete this._mediaStream), this._url && (URL.revokeObjectURL(this._url), delete this._url)
        }
        qrcode() {
          var e = this.$(io.recording),
            t = this.$(io.qrcode);
          t.classList.contains(io.hidden) ? (e.classList.add(io.hidden), t.classList.remove(io.hidden), dr
            .qrcode({
              redirect: "/mobile"
            }).then((e => this.setState("qrcode", e))).catch((e => this.params.onError(e)))) : (t.classList
            .add(io.hidden), e.classList.remove(io.hidden))
        }
        start() {
          return this._file ? this.saveRecord() : this._recorder ? this.stopRecording() : void this
            .startRecording()
        }
        retry() {
          this.params.onComplete(!1);
          var e = this.$(io.webcam);
          this._file && (this._file = null, e.src && (URL.revokeObjectURL(e.src), e.src = ""), e.srcObject =
            this._mediaStream, e.controls = !1), this._mediaStream ? (e.play(), this.setState("stage",
            "ready")) : (this.setState("stage", "loading"), delete e.dataset.off, e.dataset.spinner = !0,
            Vt(oo({
              audio: !1
            }, l.get("webcam"))).then((t => {
              this._mediaStream = t, void 0 !== e.srcObject ? e.srcObject = t : (this._url = URL
                .createObjectURL(t), e.src = this._url), e.play(), e.onplaying = () => {
                e.onplaying = null, delete e.dataset.spinner, this.setState("stage", "ready")
              }
            })).catch((t => {
              delete e.dataset.spinner, e.dataset.off = !0, this.errorHandler(t, "nocamera")
            })))
        }
        startRecording() {
          this.setState("stage", "loading");
          var e = new rr(oo({
            audioBitsPerSecond: 16384,
            videoBitsPerSecond: 131072
          }, l.get("webcam.recorder")));
          this._recorder = e;
          var t = this.$(io.webcam);
          e.start(t, "overview").then((() => {
            var t = 60;
            this.setState("stage", "recording"), this.renderTimer(t), this._timer = setInterval((() => {
              e.active && (this.renderTimer(--t), 0 === t && this.stopRecording())
            }), 1e3)
          })).catch((e => this.errorHandler(e, "norecord")))
        }
        stopRecording() {
          clearInterval(this._timer), this.setState("stage", "loading");
          var e = this._recorder;
          this._recorder = null, e.stop().then((e => {
            if (this._file = e[1], !this._file) throw Error("Record does not exist");
            var t = this.$(io.webcam);
            t && (this._mediaStream = t.srcObject, t.srcObject = null, t.src = URL.createObjectURL(this
              ._file), t.controls = !0), this.renderTimer(0), this.setState("stage", "recorded")
          })).catch((e => this.errorHandler(e, "norecord")))
        }
        saveRecord() {
          this.setState("stage", "loading"), Ee("/api/storage", {
            body: this._file
          }).then((e => {
            var t = e.id;
            return Ee("/api/room/update/".concat(sr.get("id")), {
              method: "POST",
              body: {
                overview: t
              }
            })
          })).then((() => {
            this.setState("stage", "done"), this.params.onComplete(!0)
          })).catch((e => this.errorHandler(e, "norecord")))
        }
        errorHandler(e, t) {
          this._recorder = null, this._file = null, this.setState("stage", t), this.params.onError(e)
        }
      }
      var co = r(1059),
        lo = {};
      lo.styleTagTransform = ji(), lo.setAttributes = bi(), lo.insert = hi().bind(null, "head"), lo.domAPI =
      vi(), lo.insertStyleElement = yi();
      ui()(co.Z, lo);
      const uo = co.Z && co.Z.locals ? co.Z.locals : void 0;
      class po extends pn {
        constructor() {
          var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {};
          super(e), this._eventHandler = t => {
            t && "mobile" === t.event && e.onComplete.call(this, !0)
          }, this.mount(e.el)
        }
        render() {
          var e = super.render();
          return e.className = uo.qrcode, e.innerHTML = '\n    <div class="'.concat(uo.description, '"><div>')
            .concat(Ei("qrcode.text"), '</div></div>\n    <div class="').concat(uo.separator,
              '"></div>\n    <div class="').concat(uo.body, '"><img class="').concat(uo.img,
              '" /></div>\n    '), e
        }
        updated(e, t) {
          if ("data" === e) {
            var r = this.$(uo.img);
            r.src = t.qrcode, r.title = Ei("qrcode.expires", {
              timeleft: new Date(1e3 * t.exp).toLocaleString(zi())
            })
          }
        }
        mounted() {
          Ke.on("userdata", this._eventHandler), dr.qrcode({
            redirect: "/mobile"
          }).then((e => this.setState("data", e))).catch((e => this.params.onError(e)))
        }
        removed() {
          Ke.off("userdata", this._eventHandler), delete this._eventHandler
        }
        data() {
          return {
            data: null
          }
        }
      }
      class vo extends wn {
        constructor() {
          var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {};
          if (e.disabled = !0, e._callback = e.callback, e.callback = function (e) {
              if (e) this.nextStage();
              else {
                var t = this.params._callback;
                "function" == typeof t && t.call(this, e)
              }
            }, super(e), this.state.stages.length) this.mount(e.el);
          else {
            var t = this.params._callback;
            "function" == typeof t && t.call(this, !0)
          }
        }
        renderHeader() {
          return super.renderHeader({
            title: Ei("wizard.title.".concat(this.state.stage)),
            close: !0
          })
        }
        renderBody() {
          this._view && (this._view.remove(), delete this._view);
          var e = super.renderBody(),
            t = this.state.views[this.state.stage];
          return t && (this._view = new t({
            el: e,
            onComplete: e => {
              sr.get("error") && sr.update({
                error: null
              }), this.setState("complete", e)
            },
            onError: e => sr.update({
              error: String(e)
            })
          })), e
        }
        renderFooter() {
          var e = this.state.stages.indexOf(this.state.stage) + 1,
            t = this.state.stages.length;
          return super.renderFooter({
            caption: Ei("wizard.page", {
              page: e,
              total: t
            }),
            ok: Ei("wizard.button.next"),
            disabled: this.params.disabled
          })
        }
        updated(e) {
          "stage" === e && (this.renderHeader(), this.renderBody(), this.renderFooter()), "complete" === e &&
            (this.state.complete ? this.enable() : this.disable())
        }
        removed() {
          this._view && (this._view.remove(), delete this._view)
        }
        data() {
          var e = {
              rules: sr.hasAddon("rules") ? En : null,
              check: sr.hasAddon("check") ? Qn : null,
              profile: sr.hasAddon("profile") ? Bn : null,
              face: sr.hasAddon("face") ? Zn : null,
              passport: sr.hasAddon(["passport", "scan"]) ? eo : null,
              overview: sr.hasAddon("overview") && !sr.hasAddon("qrcode") ? so : null,
              qrcode: sr.hasAddon("qrcode") ? po : null
            },
            t = Object.keys(e).filter((t => !!e[t])),
            r = t[0];
          return {
            views: e,
            stage: r,
            stages: t,
            complete: !1
          }
        }
        nextStage() {
          this._view && (this._view.remove(), delete this._view);
          var e = this.state.stages.indexOf(this.state.stage) + 1,
            t = this.state.stages[e];
          if (this.state.views[t]) this.setState("complete", !1), this.setState("stage", t);
          else {
            this.remove();
            var r = this.params._callback;
            "function" == typeof r && r.call(this, !0)
          }
        }
      }
      var mo = r(6141),
        ho = {};
      ho.styleTagTransform = ji(), ho.setAttributes = bi(), ho.insert = hi().bind(null, "head"), ho.domAPI =
      vi(), ho.insertStyleElement = yi();
      ui()(mo.Z, ho);
      const go = mo.Z && mo.Z.locals ? mo.Z.locals : void 0;
      class bo extends pn {
        constructor() {
          var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {};
          super(e), this.mount(e.el), this.startTimer()
        }
        render() {
          var e = this.params.onclick || function () {},
            t = super.render();
          t.className = go.toolbar;
          var r = document.createElement("div");
          r.className = go.border, t.appendChild(r);
          var i = document.createElement("div");
          i.className = go.timer, t.appendChild(i);
          var n = document.createElement("div");
          n.className = go.tooltip, n.style.display = "none", n.addEventListener("click", (t => {
            e({
              type: "tooltip",
              target: n
            }), this.setText(), t.preventDefault()
          }), !1), t.appendChild(n);
          var o = document.createElement("div");
          if (o.className = go.tools, sr.hasAddon("finish")) {
            var a = document.createElement("div");
            a.className = go.btn, a.classList.add(go.exit), a.addEventListener("click", (() => {
              e({
                type: "exit",
                target: a
              })
            }), !1), o.appendChild(a)
          }
          if (sr.hasAddon("chat")) {
            var s = document.createElement("div");
            s.className = go.btn, s.classList.add(go.chat), s.addEventListener("click", (() => {
              e({
                type: "chat",
                target: s
              })
            }), !1), o.appendChild(s)
          }
          if (sr.hasAddon("qrcode")) {
            var c = document.createElement("div");
            c.className = go.btn, c.classList.add(go.qrcode), c.addEventListener("click", (() => {
              e({
                type: "qrcode",
                target: c
              })
            }), !1), o.appendChild(c)
          }
          if (sr.hasAddon("calculator")) {
            var l = document.createElement("div");
            l.className = go.btn, l.classList.add(go.calc), l.addEventListener("click", (() => {
              e({
                type: "calc",
                target: l
              })
            }), !1), o.appendChild(l)
          }
          if (o.firstChild) {
            var d = document.createElement("input");
            d.className = go.trigger, d.type = "checkbox", t.appendChild(d);
            var u = document.createElement("label");
            u.setAttribute("for", go.trigger), u.addEventListener("click", (e => {
                h || e.defaultPrevented || (d.checked = !d.checked)
              }), !1), sr.hasAddon("toolbox") && (u.style.visibility = "visible"), t.appendChild(u), t
              .appendChild(o)
          }
          var p = {
              left: t.style.left,
              right: t.style.right,
              top: t.style.top,
              bottom: t.style.bottom
            },
            v = [0, 0],
            m = !1,
            h = !1;
          return this._onmousedown = e => {
            var r = e.changedTouches || [{}],
              i = r[0].clientX || e.clientX,
              n = r[0].clientY || e.clientY;
            m = !0, h = !1, v = [t.offsetLeft - i, t.offsetTop - n]
          }, t.addEventListener("mousedown", this._onmousedown, !0), t.addEventListener("touchstart", this
            ._onmousedown, !0), this._onmouseup = () => {
            m = !1
          }, document.addEventListener("mouseup", this._onmouseup, !0), document.addEventListener(
            "touchend", this._onmouseup, !0), this._onmousemove = e => {
            if (h = !0, m) {
              var r = e.changedTouches || [{}],
                i = r[0].clientX || e.clientX,
                n = r[0].clientY || e.clientY,
                o = i + v[0],
                a = n + v[1];
              o < 0 && (o = 0), a < 0 && (a = 0), o + t.offsetWidth > window.innerWidth && (o = window
                  .innerWidth - t.offsetWidth), a + t.offsetHeight > window.innerHeight && (a = window
                  .innerHeight - t.offsetHeight), t.style.left = o + "px", t.style.top = a + "px", this
                .updateTooltipPos()
            }
          }, document.addEventListener("mousemove", this._onmousemove, !0), document.addEventListener(
            "touchmove", this._onmousemove, !0), this._onresize = () => {
            t.style.left = p.left, t.style.right = p.right, t.style.top = p.top, t.style.bottom = p.bottom,
              this.updateTooltipPos()
          }, window.addEventListener("resize", this._onresize, !1), t
        }
        removed() {
          this._timer && (clearInterval(this._timer), delete this._timer), this._onmousedown && (this.el
            .removeEventListener("mousedown", this._onmousedown), this.el.removeEventListener("touchstart",
              this._onmousedown), delete this._onmousedown), this._onmouseup && (document
            .removeEventListener("mouseup", this._onmouseup), document.removeEventListener("touchend", this
              ._onmouseup), delete this._onmouseup), this._onmousemove && (document.removeEventListener(
              "mousemove", this._onmousemove), document.removeEventListener("touchmove", this._onmousemove),
            delete this._onmousemove), this._onresize && (window.removeEventListener("resize", this
            ._onresize), delete this._onresize)
        }
        setVideo(e) {
          if ([].forEach.call(this.el.childNodes || [], (function (e) {
              "VIDEO" === e.tagName && e.remove()
            })), e instanceof HTMLVideoElement) this.el.appendChild(e);
          else if ("object" == typeof e) {
            Xt({
              spinner: !0,
              mirror: !0,
              muted: !0
            }).srcObject = e, this.el.appendChild(e)
          }
        }
        setHightlight() {
          var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : 100;
          this._timer || (e > 100 ? e = 100 : e < 0 && (e = 0), this.$(go.border).style.background = "hsl("
            .concat(e, ",90%,50%)"))
        }
        setText(e, t, r) {
          e = e || "";
          var i = this.$(go.tooltip);
          t ? i.dataset.id = t : delete i.dataset.id, r ? i.classList.add(go.danger) : i.classList.remove(go
              .danger), i.innerHTML = t ? "".concat(e, '<span class="').concat(go.btn, '"></span>') : ""
            .concat(e), this.updateTooltipPos()
        }
        startTimer() {
          var e, t = this.$(go.border),
            r = this.$(go.timer),
            i = sr.get("startedAt"),
            n = sr.get("lifetime"),
            o = sr.get("deadline"),
            a = sr.get("timeout");
          if (o && !a && (e = new Date(o).getTime()), n) {
            var s = new Date(i).getTime() + 60 * n * 1e3;
            (!e || e > s) && (e = s)
          }
          if (e) {
            var c = new Date(i).getTime();
            this._timer = setInterval((() => {
              var i = (Date.now() - c) / (e - c);
              i < 0 && (i = 0), i > 1 && (i = 1);
              var n = ~~(360 * i);
              t.style.background = "conic-gradient(var(--warning-color) ".concat(n,
                "deg, var(--info-color) 0deg)");
              var o = e - Date.now();
              o < 0 && (o = 0), r.innerText = new Date(o).toISOString().substring(11, 19)
            }), 1e3)
          }
        }
        updateTooltipPos() {
          var e = this.el,
            t = this.$(go.tooltip);
          0 !== e.offsetWidth || 0 !== e.offsetHeight ? (t.innerText ? t.style.display = "" : t.style
            .display = "none", e.offsetLeft + e.offsetWidth / 2 < window.innerWidth / 2 ? (t.classList.add(
              go.tooltip_right), t.classList.remove(go.tooltip_left)) : (t.classList.add(go.tooltip_left), t
              .classList.remove(go.tooltip_right))) : t.style.display = "none"
        }
      }
      var fo = r(5501),
        yo = {};
      yo.styleTagTransform = ji(), yo.setAttributes = bi(), yo.insert = hi().bind(null, "head"), yo.domAPI =
      vi(), yo.insertStyleElement = yi();
      ui()(fo.Z, yo);
      const Mo = fo.Z && fo.Z.locals ? fo.Z.locals : void 0;
      class jo extends pn {
        constructor() {
          var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {};
          super(e), this._messageHandler = this.messageHandler.bind(this), this._pasteHandler = this
            .pasteHandler.bind(this), this._reloadHandler = () => this.loadMessages(), this.mount(e.el)
        }
        render() {
          var e = super.render();
          e.className = Mo.chat, e.style.display = "none", e.innerHTML = '\n    <div class="'.concat(Mo
              .header, '">\n      <div class="').concat(Mo.title, '">').concat(Ei("chat.title"),
              '</div>\n      <div class="').concat(Mo.close_btn, '"></div>\n    </div>\n    <div class="')
            .concat(Mo.player, '"></div>\n    <div class="').concat(Mo.body, '"></div>\n    <div class="')
            .concat(Mo.files, '"></div>\n    <div class="').concat(Mo.footer, '">\n      <textarea class="')
            .concat(Mo.input_text, '"\n        placeholder="').concat(Ei("chat.inputPlaceholder"),
              '"></textarea>\n      <div class="').concat(Mo.buttons, '">\n        <div class="').concat(Mo
              .send_btn, '"></div>\n        <div class="').concat(Mo.clip_btn,
              '"></div>\n        <input class="').concat(Mo.input_file,
              '" type="file"/>\n      </div>\n    </div>\n    ');
          var t = this.params.player;
          if (t) {
            var r = this.$(Mo.player, e);
            t.classList.add(Mo.player), r.parentNode.replaceChild(t, r)
          }
          return sr.hasAddon("upload") || this.$(Mo.clip_btn, e).remove(), e
        }
        renderMessage(e) {
          var t, r, i = document.createElement("DIV");
          i.className = "".concat(Mo.item, " ").concat(Re.isMe(e.author && e.author.id) ? Mo.right : Mo.left),
            e.metadata && e.metadata.incident && (i.className += " ".concat(Mo.highlight));
          var n, o, a, s, c = (null === (t = e.author) || void 0 === t ? void 0 : t.nickname) || (null === (
              r = e.author) || void 0 === r ? void 0 : r.username) || "???",
            l = e.text ? '<div class="'.concat(Mo.text, '">').concat(function (e) {
              return "".concat(e).replace(
                /\b(?:https?):\/\/[a-z0-9-+&@#/%?=~_|!:,.;]*[a-z0-9-+&@#/%=~_|]/gim,
                '<a target="_blank" href="$&">$&</a>')
            }(function (e) {
              return "".concat(e).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
                .replace(/"/g, "&quot;").replace(/'/g, "&apos;")
            }(e.text)), "</div>") : "";
          return i.innerHTML = '\n      <div class="'.concat(Mo.caption, '">\n        <div class="').concat(Mo
            .user, '">').concat(c, '</div>\n        <div class="').concat(Mo.time, '">').concat((n = e
            .createdAt, o = new Date(n), a = ("0" + o.getHours()).slice(-2), s = ("0" + o.getMinutes())
            .slice(-2), "".concat(a, ":").concat(s)), '</div>\n      </div>\n      <div class="').concat(Mo
            .message, '">\n        ').concat(l, "\n        ").concat(this.renderAttaches(e.attach),
            "\n      </div>\n    "), i
        }
        renderAttaches(e) {
          return e.map((function (e) {
            return /image\//.test(e.mimetype) ? '<div class="'.concat(Mo.attach,
                '">\n          <a class="').concat(Mo.link, '" href="').concat(Ee.url, "/api/storage/")
              .concat(e.id, '"\n            download="').concat(e.filename, '" title="').concat(e
                .filename, '">\n          <img src="').concat(Ee.url, "/api/storage/").concat(e.id,
                "?token=").concat(Ee.token, '"\n            alt="').concat(e.filename,
                '" loading="lazy"></a>\n          </div>') : /video\//.test(e.mimetype) ? '<div class="'
              .concat(Mo.attach_icon, '">\n          <video controls preload="none" src="').concat(Ee
                .url, "/api/storage/").concat(e.id, "?token=").concat(Ee.token, '"\n            alt="')
              .concat(e.filename, '">\n          </div>') : '<div class="'.concat(Mo.attach,
                '">\n          <span class="').concat(Mo.attach_icon, '"></span>\n          <a class="')
              .concat(Mo.link, '" href="').concat(Ee.url, "/api/storage/").concat(e.id,
                '"\n            download="').concat(e.filename, '" title="').concat(e.filename,
                '">\n              ').concat(Ne(e.filename, 25, !0), "</a>\n          </div>")
          })).join("")
        }
        data() {
          return {
            text: "",
            count: 0,
            messageIds: new Set,
            files: []
          }
        }
        events() {
          return {
            click: {
              [Mo.link]: (e, t) => {
                e.preventDefault(), window.open("".concat(t.href, "?token=").concat(Ee.token))
              },
              [Mo.send_btn]: () => {
                this.sendMessage()
              },
              [Mo.clip_btn]: () => {
                if (!(this.state.files.length >= 3)) {
                  var e = document.createEvent("MouseEvents"),
                    t = this.$(Mo.input_file);
                  e.initEvent("click", !1, !1), t.dispatchEvent(e)
                }
              },
              [Mo.close_btn]: () => {
                this.hide()
              }
            },
            keydown: {
              [Mo.input_text]: e => {
                13 !== e.keyCode || e.shiftKey || (e.preventDefault(), this.sendMessage())
              }
            },
            input: {
              [Mo.input_text]: (e, t) => {
                this.setState("text", t.value)
              }
            },
            change: {
              [Mo.input_file]: (e, t) => {
                this.selectFile(t.files[0])
              }
            },
            scroll: {
              [Mo.body]: (e, t) => {
                0 === t.scrollTop && this.loadMessages(this.state.count)
              }
            }
          }
        }
        mounted() {
          Ke.on("chat:message", this._messageHandler), Ke.on("connect", this._reloadHandler), window
            .addEventListener("paste", this._pasteHandler), this.loadMessages()
        }
        updated(e, t) {
          "text" === e && (this.$(Mo.input_text).value = t)
        }
        removed() {
          Ke.off("chat:message", this._messageHandler), Ke.off("connect", this._reloadHandler), window
            .removeEventListener("paste", this._pasteHandler)
        }
        loadMessages() {
          var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : 0,
            t = this.$(Mo.body),
            r = t.firstChild;
          Ee("/api/chat/".concat(sr.get("id"), "?filter[type]=message&limit=20&skip=").concat(e)).then((i => {
            if (i.length) {
              if (function (e) {
                  e.sort((function (e, t) {
                    return e.createdAt === t.createdAt ? 0 : e.createdAt > t.createdAt ? 1 : -1
                  }))
                }(i), e && r) i.forEach((e => {
                t.insertBefore(this.renderMessage(e), r)
              })), this.scrollDown(30);
              else if (t.innerHTML = "", i.forEach((e => {
                  t.appendChild(this.renderMessage(e))
                })), Date.now() - new Date(i[i.length - 1].createdAt).getTime() < 6e4 && this.show(),
                this.params.onincident) {
                var n, o = i[i.length - 1];
                "boolean" == typeof (null == o || null === (n = o.metadata) || void 0 === n ? void 0 : n
                  .incident) && this.params.onincident(o.metadata.incident)
              }
              this.state.count += i.length
            }
          }))
        }
        messageHandler(e) {
          e.room === sr.get("id") && "message" === e.type && this.appendMessage(e)
        }
        pasteHandler(e) {
          if (e.clipboardData && e.target && "TEXTAREA" === e.target.tagName) {
            var t = e.clipboardData.items;
            if (t)
              for (var r = 0; r < t.length; r++)
                if ("image/png" === t[r].type) {
                  var i = t[r].getAsFile();
                  this.selectFile(i)
                }
          }
        }
        appendMessage(e) {
          this.state.messageIds.has(e.id) || (this.state.messageIds.add(e.id), this.$(Mo.body).appendChild(
              this.renderMessage(e)), this.state.count++, this.show(), this.params.onincident && e
            .metadata && "boolean" == typeof e.metadata.incident && this.params.onincident(e.metadata
              .incident))
        }
        sendMessage() {
          var e = this.state.text,
            t = this.state.files;
          (e || t.length) && (Ee("/api/chat/".concat(sr.get("id")), {
            method: "POST",
            body: {
              type: "message",
              text: e,
              attach: this.getAttach()
            }
          }).then((e => {
            this.setState("text", ""), this.clearFiles(), this.appendMessage(e)
          })).catch((() => {
            this.setState("text", e)
          })), this.setState("text", ""))
        }
        scrollDown(e) {
          var t = this.$(Mo.body);
          t.scrollTop = e || (t.lastChild || {}).offsetTop
        }
        selectFile(e) {
          if (e) {
            var t = new Po({
              el: this.$(Mo.files),
              file: e,
              removed: () => {
                var e = this.state.files,
                  r = e.findIndex((e => e === t));
                r > -1 && e.splice(r, 1)
              }
            });
            this.state.files.push(t)
          }
        }
        clearFiles() {
          for (var e = this.state.files.slice(), t = 0; t < e.length; t++) e[t].remove()
        }
        getAttach() {
          return this.state.files.map((function (e) {
            return e.state.attach.id
          }))
        }
        show() {
          this.el.style.display = "", this.scrollDown()
        }
        hide() {
          this.el.style.display = "none"
        }
        toggle() {
          "none" !== this.el.style.display ? this.hide() : this.show()
        }
      }
      class Po extends pn {
        constructor() {
          var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {};
          super(e), this.removed = e.removed, this.mount(e.el)
        }
        render() {
          var e = document.createElement("DIV"),
            t = this.params.file;
          return e.className = Mo.file, e.innerHTML = '\n      <div class="'.concat(Mo.filename,
            '">\n        <div title="').concat(t.name, '">').concat(Ne(t.name, 25, !0),
            '</div>\n        <div class="').concat(Mo.progress,
            '" style="width: 0"></div>\n      </div>\n      <div class="').concat(Mo.remove,
            '"></div>\n    '), e
        }
        updated(e, t) {
          if ("progress" === e && (this.$(Mo.progress).style.width = "".concat(t || 0, "%")), "status" ===
            e) {
            var r = this.$(Mo.filename);
            "done" === t && (r.className = "".concat(Mo.filename, " ").concat(Mo.progress_done)), "error" ===
              t && (r.className = "".concat(Mo.filename, " ").concat(Mo.progress_err))
          }
        }
        mounted() {
          var e = l.get("upload.limit") || 5,
            t = this.params.file;
          t.size > 1024 * e * 1024 ? this.setState("status", "error") : Ee("/api/storage", {
            body: t,
            progress: e => {
              var t = Math.round(e.loaded / e.total * 100);
              this.setState("progress", t)
            }
          }).then((e => {
            this.setState("attach", e), this.setState("progress", 0), this.setState("status", "done")
          })).catch((() => {
            this.setState("progress", 0), this.setState("status", "error")
          }))
        }
        data() {
          return {
            progress: 0,
            status: ""
          }
        }
        events() {
          return {
            click: {
              [Mo.remove]: (e, t) => {
                this.remove()
              }
            }
          }
        }
      }
      var To = r(8088),
        Lo = {};
      Lo.styleTagTransform = ji(), Lo.setAttributes = bi(), Lo.insert = hi().bind(null, "head"), Lo.domAPI =
      vi(), Lo.insertStyleElement = yi();
      ui()(To.Z, Lo);
      const Ao = To.Z && To.Z.locals ? To.Z.locals : void 0;
      class wo extends pn {
        constructor() {
          var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {};
          super(e), this.mount(e.el)
        }
        render() {
          var e = document.createElement("DIV");
          e.className = Ao.calc, e.style.display = "none", e.innerHTML = '\n<div class="'.concat(Ao.header,
              '">\n  <div class="').concat(Ao.title, '">').concat(Ei("calculator.title"),
              '</div>\n  <div class="').concat(Ao.close_btn, '"></div>\n</div>\n<div class="').concat(Ao.body,
              '">\n  <div class="').concat(Ao.output, '">\n    <input class="').concat(Ao.input,
              '" value="0"></input>\n  </div>\n  <div class="').concat(Ao.block, '">\n    <div class="')
            .concat(Ao.line, '">\n      <div data-key="sin" class="').concat(Ao.scifunc, " ").concat(Ao.rfunc,
              '">sin</div>\n      <div data-key="cos" class="').concat(Ao.scifunc, " ").concat(Ao.rfunc,
              '">cos</div>\n      <div data-key="tan" class="').concat(Ao.scifunc, " ").concat(Ao.rfunc,
              '">tan</div>\n      <div class="').concat(Ao.scird, '">\n        <input class="').concat(Ao
              .scirdsettingd,
              '" type="radio" name="scirdsettings" value="deg" checked="checked"><label><span><span></span></span>Deg</label>\n        <input class="'
              ).concat(Ao.scirdsettingr,
              '" type="radio" name="scirdsettings" value="rad"><label><span><span></span></span>Rad</label>\n      </div>\n    </div>\n    <div class="'
              ).concat(Ao.line, '">\n      <div data-key="asin" class="').concat(Ao.scifunc, " ").concat(Ao
              .rfunc, '">sin<sup>-1</sup></div>\n      <div data-key="acos" class="').concat(Ao.scifunc, " ")
            .concat(Ao.rfunc, '">cos<sup>-1</sup></div>\n      <div data-key="atan" class="').concat(Ao
              .scifunc, " ").concat(Ao.rfunc, '">tan<sup>-1</sup></div>\n      <div data-key="pi" class="')
            .concat(Ao.scifunc, " ").concat(Ao.rfunc, '">&#960;</div>\n      <div data-key="e" class="')
            .concat(Ao.scifunc, " ").concat(Ao.rfunc, '">e</div>\n    </div>\n    <div class="').concat(Ao
              .line, '">\n      <div data-key="pow" class="').concat(Ao.scifunc, " ").concat(Ao.rfunc,
              '">x<sup>y</sup></div>\n      <div data-key="x3" class="').concat(Ao.scifunc, " ").concat(Ao
              .rfunc, '">x<sup>3</sup></div>\n      <div data-key="x2" class="').concat(Ao.scifunc, " ")
            .concat(Ao.rfunc, '">x<sup>2</sup></div>\n      <div data-key="ex" class="').concat(Ao.scifunc,
              " ").concat(Ao.rfunc, '">e<sup>x</sup></div>\n      <div data-key="10x" class="').concat(Ao
              .scifunc, " ").concat(Ao.rfunc, '">10<sup>x</sup></div>\n    </div>\n    <div class="').concat(
              Ao.line, '">\n      <div data-key="apow" class="').concat(Ao.scifunc, " ").concat(Ao.rfunc,
              '"><sup>y</sup>&#8730;x</div>\n      <div data-key="3x" class="').concat(Ao.scifunc, " ")
            .concat(Ao.rfunc, '"><sup>3</sup>&#8730;x</div>\n      <div data-key="sqrt" class="').concat(Ao
              .scifunc, " ").concat(Ao.rfunc, '">&#8730;x</div>\n      <div data-key="ln" class="').concat(Ao
              .scifunc, " ").concat(Ao.rfunc, '">ln</div>\n      <div data-key="log" class="').concat(Ao
              .scifunc, " ").concat(Ao.rfunc, '">log</div>\n    </div>\n    <div class="').concat(Ao.line,
              '">\n      <div data-key="(" class="').concat(Ao.scifunc, " ").concat(Ao.rfunc,
              '">(</div>\n      <div data-key=")" class="').concat(Ao.scifunc, " ").concat(Ao.rfunc,
              '">)</div>\n      <div data-key="1/x" class="').concat(Ao.scifunc, " ").concat(Ao.rfunc,
              '">1/x</div>\n      <div data-key="pc" class="').concat(Ao.scifunc, " ").concat(Ao.rfunc,
              '">%</div>\n      <div data-key="n!" class="').concat(Ao.scifunc, " ").concat(Ao.rfunc,
              '">n!</div>\n    </div>\n  </div>\n  <div class="').concat(Ao.block, '">\n    <div class="')
            .concat(Ao.line, '">\n      <div data-key="7" class="').concat(Ao.scinm, " ").concat(Ao.rfunc,
              '">7</div>\n      <div data-key="8" class="').concat(Ao.scinm, " ").concat(Ao.rfunc,
              '">8</div>\n      <div data-key="9" class="').concat(Ao.scinm, " ").concat(Ao.rfunc,
              '">9</div>\n      <div data-key="+" class="').concat(Ao.sciop, " ").concat(Ao.rfunc,
              '">+</div>\n      <div data-key="MS" class="').concat(Ao.sciop, " ").concat(Ao.rfunc,
              '">MS</div>\n    </div>\n    <div class="').concat(Ao.line,
              '">\n      <div data-key="4" class="').concat(Ao.scinm, " ").concat(Ao.rfunc,
              '">4</div>\n      <div data-key="5" class="').concat(Ao.scinm, " ").concat(Ao.rfunc,
              '">5</div>\n      <div data-key="6" class="').concat(Ao.scinm, " ").concat(Ao.rfunc,
              '">6</div>\n      <div data-key="-" class="').concat(Ao.sciop, " ").concat(Ao.rfunc,
              '">&ndash;</div>\n      <div data-key="M+" class="').concat(Ao.sciop, " ").concat(Ao.rfunc,
              '">M+</div>\n    </div>\n    <div class="').concat(Ao.line,
              '">\n      <div data-key="1" class="').concat(Ao.scinm, " ").concat(Ao.rfunc,
              '">1</div>\n      <div data-key="2" class="').concat(Ao.scinm, " ").concat(Ao.rfunc,
              '">2</div>\n      <div data-key="3" class="').concat(Ao.scinm, " ").concat(Ao.rfunc,
              '">3</div>\n      <div data-key="*" class="').concat(Ao.sciop, " ").concat(Ao.rfunc,
              '">&#215;</div>\n      <div data-key="M-" class="').concat(Ao.sciop, " ").concat(Ao.rfunc,
              '">M-</div>\n    </div>\n    <div class="').concat(Ao.line,
              '">\n      <div data-key="0" class="').concat(Ao.scinm, " ").concat(Ao.rfunc,
              '">0</div>\n      <div data-key="." class="').concat(Ao.scinm, " ").concat(Ao.rfunc,
              '">.</div>\n      <div data-key="EXP" class="').concat(Ao.sciop, " ").concat(Ao.rfunc,
              '">EXP</div>\n      <div data-key="/" class="').concat(Ao.sciop, " ").concat(Ao.rfunc,
              '">&#247;</div>\n      <div data-key="MR" class="').concat(Ao.sciop, " ").concat(Ao.rfunc,
              '">MR</div>\n    </div>\n    <div class="').concat(Ao.line,
              '">\n      <div data-key="+/-" class="').concat(Ao.sciop, " ").concat(Ao.rfunc,
              '">&#177;</div>\n      <div data-key="RND" class="').concat(Ao.sciop, " ").concat(Ao.rfunc,
              '">RND</div>\n      <div data-key="C" class="').concat(Ao.scieq, " ").concat(Ao.rfunc,
              '">C</div>\n      <div data-key="=" class="').concat(Ao.scieq, " ").concat(Ao.rfunc,
              '">=</div>\n      <div data-key="MC" class="').concat(Ao.sciop, " ").concat(Ao.rfunc,
              '">MC</div>\n    </div>\n  </div>\n</div>');
          var t = 0,
            r = 0,
            i = [0, 0],
            n = !1,
            o = this.$(Ao.header, e),
            a = this.$(Ao.input, e);
          return this._onkeydown = e => {
            switch (e.preventDefault(), e.keyCode) {
            case 8:
              this.r("C");
              break;
            case 13:
              this.r("=");
              break;
            default:
              this.r(e.key)
            }
          }, a.addEventListener("keydown", this._onkeydown), this._onmousedown = function (t) {
            var r = t.changedTouches || [{}],
              o = r[0].clientX || t.clientX,
              a = r[0].clientY || t.clientY;
            n = !0, i = [e.offsetLeft - o, e.offsetTop - a]
          }, o.addEventListener("mousedown", this._onmousedown, !0), o.addEventListener("touchstart", this
            ._onmousedown, !0), this._onmouseup = function () {
            n = !1
          }, document.addEventListener("mouseup", this._onmouseup, !0), document.addEventListener(
            "touchend", this._onmouseup, !0), this._onmousemove = function (t) {
            if (n) {
              var r = t.changedTouches || [{}],
                o = r[0].clientX || t.clientX,
                a = r[0].clientY || t.clientY,
                s = o + i[0],
                c = a + i[1];
              s < 0 && (s = 0), c < 0 && (c = 0), s + e.offsetWidth > window.innerWidth && (s = window
                .innerWidth - e.offsetWidth), c + e.offsetHeight > window.innerHeight && (c = window
                .innerHeight - e.offsetHeight), e.style.left = s + "px", e.style.top = c + "px"
            }
          }, document.addEventListener("mousemove", this._onmousemove, !0), document.addEventListener(
            "touchmove", this._onmousemove, !0), this._onresize = function () {
            e.style.left = t, e.style.top = r
          }, window.addEventListener("resize", this._onresize, !1), e
        }
        mounted() {
          var e = "degree",
            t = 0,
            r = 0,
            i = 0,
            n = !0,
            o = 0,
            a = 0,
            s = !1,
            c = 0,
            l = 0,
            d = new function (e) {
              this[0] = 0;
              for (var t = 0; t < e; ++t) this[t] = 0, this[t] = new p;
              this.gG = e
            }(12),
            u = this.$.bind(this);
  
          function p() {
            this.value = 0, this.op = ""
          }
  
          function v(e, t, r) {
            if (12 == i) return !1;
            for (var n = i; n > 0; --n) d[n].value = d[n - 1].value, d[n].op = d[n - 1].op, d[n].vg = d[n - 1]
              .vg;
            return d[0].value = e, d[0].op = t, d[0].vg = r, ++i, !0
          }
  
          function m() {
            var e = function (e) {
              if ("undefined" == typeof cc) {
                var t = "" + e;
                if (t.indexOf("N") >= 0 || e == 2 * e && e == 1 + e) return "Error ";
                var r = t.indexOf("e");
                if (r >= 0) {
                  var i = t.substring(r + 1, t.length);
                  if (r > 11 && (r = 11), (t = t.substring(0, r)).indexOf(".") < 0) t += ".";
                  else {
                    for (var o = t.length - 1; o >= 0 && "0" == t.charAt(o);) --o;
                    t = t.substring(0, o + 1)
                  }
                  t += " " + i
                } else {
                  var s = !1;
                  e < 0 && (e = -e, s = !0);
                  var c = Math.floor(e),
                    l = e - c,
                    d = 12 - ("" + c).length - 1;
                  !n && a > 0 && (d = a);
                  var u = " 1000000000000000000".substring(1, d + 2) + "";
                  u = "" == u || " " == u ? 1 : parseInt(u);
                  var p = Math.floor(l * u + .5);
                  c = Math.floor(Math.floor(e * u + .5) / u), t = s ? "-" + c : "" + c;
                  var v = "00000000000000" + p;
                  if (r = (v = v.substring(v.length - d, v.length)).length - 1, n || 0 == a) {
                    for (; r >= 0 && "0" == v.charAt(r);) --r;
                    v = v.substring(0, r + 1)
                  }
                  r >= 0 && (t += "." + v)
                }
                return t
              }
            }(t);
            s && (e += l < 0 ? " " + l : " +" + l), e.indexOf(".") < 0 && "Error " != e && (e += n || o > 0 ?
              "." : " "), u(Ao.input).value = "" + e == "" ? "" : e
          }
  
          function h() {
            if (0 == i) return !1;
            var e = d[0].op,
              r = d[0].value;
            return "+" == e ? t = parseFloat(r) + t : "-" == e ? t = r - t : "*" == e ? t *= r : "/" == e ?
              t = r / t : "pow" == e ? t = Math.pow(r, t) : "apow" == e && (t = Math.pow(r, 1 / t)),
              function () {
                if (0 == i) return !1;
                for (var e = 0; e < i; ++e) d[e].value = d[e + 1].value, d[e].op = d[e + 1].op, d[e].vg = d[
                  e + 1].vg
              }(), "(" != e
          }
  
          function g() {
            s && (t *= Math.exp(l * Math.LN10)), n = !0, s = !1, o = 0, a = 0
          }
          this.setDegreeRadians = t => {
            e = t
          }, this.r = u => {
            if ("10x" == u || "log" == u || "ex" == u || "ln" == u || "sin" == u || "asin" == u || "cos" ==
              u || "acos" == u || "tan" == u || "atan" == u || "e" == u || "pi" == u || "n!" == u || "x2" ==
              u || "1/x" == u || "swap" == u || "x3" == u || "3x" == u || "RND" == u || "M-" == u || "qc" ==
              u || "MC" == u || "MR" == u || "MS" == u || "M+" == u || "sqrt" == u || "pc" == u) !
              function (i) {
                g(), "1/x" == i && (t = 1 / t);
                "pc" == i && (t /= 100);
                if ("qc" == i) t /= 1e3;
                else if ("swap" == i) {
                  var n = t;
                  t = d[0].value, d[0].value = n
                } else {
                  var o;
                  if ("n!" == i)
                    if (t < 0 || t > 200 || t != Math.round(t)) t = "NAN";
                    else {
                      var a, s = 1;
                      for (a = 1; a <= t; ++a) s *= a;
                      t = s
                    }
                  else if ("MR" == i) t = r;
                  else if ("M+" == i) r += t;
                  else if ("MS" == i) r = t;
                  else if ("MC" == i) r = 0;
                  else if ("M-" == i) r -= t;
                  else if ("asin" == i) t = "degree" == e ? 180 * Math.asin(t) / Math.PI : Math.asin(t);
                  else if ("acos" == i) t = "degree" == e ? 180 * Math.acos(t) / Math.PI : Math.acos(t);
                  else if ("atan" == i) t = "degree" == e ? 180 * Math.atan(t) / Math.PI : Math.atan(t);
                  else if ("e^x" == i) t = Math.exp(t * Math.LN10);
                  else if ("2^x" == i) t = Math.exp(t * Math.LN2);
                  else if ("e^x" == i) t = Math.exp(t);
                  else if ("x^2" == i) t *= t;
                  else if ("e" == i) t = Math.E;
                  else if ("ex" == i) t = Math.pow(Math.E, t);
                  else if ("10x" == i) t = Math.pow(10, t);
                  else if ("x3" == i) t *= t * t;
                  else if ("3x" == i) t = Math.pow(t, 1 / 3);
                  else if ("x2" == i) t *= t;
                  else if ("sin" == i) t = "degree" == e ? Math.sin(t / 180 * Math.PI) : Math.sin(t);
                  else if ("cos" == i) "degree" == e ? ((o = t % 360) < 0 && (o += 360), t = 90 == o ||
                    270 == o ? 0 : Math.cos(t / 180 * Math.PI)) : ((o = 180 * t / Math.PI % 360) < 0 && (
                    o += 360), t = Math.abs(o - 90) < 1e-10 || Math.abs(o - 270) < 1e-10 ? 0 : Math.cos(
                    t));
                  else "tan" == i ? t = "degree" == e ? Math.tan(t / 180 * Math.PI) : Math.tan(t) : "log" ==
                    i ? t = Math.log(t) / Math.LN10 : "log2" == i ? t = Math.log(t) / Math.LN2 : "ln" == i ?
                    t = Math.log(t) : "sqrt" == i ? t = Math.sqrt(t) : "pi" == i ? t = Math.PI : "RND" ==
                    i && (t = Math.random())
                }
                m()
              }(u);
            else if (1 == u || 2 == u || 3 == u || 4 == u || 5 == u || 6 == u || 7 == u || 8 == u || 9 ==
              u || 0 == u) ! function (e) {
              n && (t = 0, c = 0, n = !1);
              if (0 == e && 0 == c) return void m();
              if (s) return l < 0 && (e = -e), void(c < 3 && (l = 10 * l + e, ++c, m()));
              t < 0 && (e = -e);
              c < 11 && (++c, o > 0 ? (t += e / (o *= 10), ++a) : t = 10 * t + e);
              m()
            }(parseInt(u));
            else if ("pow" == u || "apow" == u || "+" == u || "-" == u || "*" == u || "/" == u) ! function (
              e) {
              var r;
              g(), "+" == e || "-" == e ? r = 1 : "*" == e || "/" == e ? r = 2 : "pow" != e && "apow" !=
                e || (r = 3);
              i > 0 && r <= d[0].vg && h();
              v(t, e, r) || (t = "NAN");
              m()
            }(u);
            else if ("(" == u) ! function () {
              g(), v(0, "(", 0) || (t = "NAN");
              m()
            }();
            else if (")" == u) ! function () {
              g();
              for (; h(););
              m()
            }();
            else if ("EXP" == u) ! function () {
              if (n || s) return;
              s = !0, l = 0, c = 0, o = 0, m()
            }();
            else if ("." == u) n && (t = 0, c = 1), n = !1, 0 == o && 0 == t && 0 == c && (c = 1), 0 == o &&
              (o = 1), m();
            else if ("+/-" == u) s ? l = -l : t = -t, m();
            else if ("C" == u) i = 0, s = !1, t = 0, g(), m();
            else if ("=" == u) {
              for (g(); i > 0;) h(), --i;
              m()
            }
          }
        }
        removed() {
          this._onkeydown && (this.$(Ao.input).removeEventListener("keydown", this._onmousedown), delete this
            ._onkeydown);
          if (this._onmousedown) {
            var e = this.$(Ao.header);
            e.removeEventListener("mousedown", this._onmousedown), e.removeEventListener("touchstart", this
              ._onmousedown), delete this._onmousedown
          }
          this._onmouseup && (document.removeEventListener("mouseup", this._onmouseup), document
              .removeEventListener("touchend", this._onmouseup), delete this._onmouseup), this._onmousemove &&
            (document.removeEventListener("mousemove", this._onmousemove), document.removeEventListener(
              "touchmove", this._onmousemove), delete this._onmousemove), this._onresize && (window
              .removeEventListener("resize", this._onresize), delete this._onresize)
        }
        events() {
          return {
            click: {
              [Ao.rfunc]: (e, t) => {
                this.r(t.dataset.key)
              },
              [Ao.scirdsettingd]: () => {
                this.setDegreeRadians("degree")
              },
              [Ao.scirdsettingr]: () => {
                this.setDegreeRadians("radians")
              },
              [Ao.close_btn]: () => {
                this.hide()
              }
            }
          }
        }
        show() {
          if (this.el.style.display = "", !this.el.style.left) {
            var e = ~~((window.innerWidth || 0) / 2 - (this.el.clientWidth || 0) / 2);
            this.el.style.left = e + "px"
          }
          if (!this.el.style.top) {
            var t = ~~((window.innerHeight || 0) / 2 - (this.el.clientHeight || 0) / 2);
            this.el.style.top = t + "px"
          }
        }
        hide() {
          this.el.style.display = "none"
        }
        toggle() {
          this.el.style.display ? this.show() : this.hide()
        }
      }
      var ko = r(6605),
        No = {};
      No.styleTagTransform = ji(), No.setAttributes = bi(), No.insert = hi().bind(null, "head"), No.domAPI =
      vi(), No.insertStyleElement = yi();
      ui()(ko.Z, No);
      const Io = ko.Z && ko.Z.locals ? ko.Z.locals : void 0;
      class Do extends wn {
        constructor() {
          var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {};
          e.disabled = !0, e._callback = e.callback, e.callback = e => this.start(e), super(e), this.mount(e
            .el)
        }
        renderHeader() {
          return super.renderHeader({
            title: Ei("ready.title"),
            close: !0
          })
        }
        renderBody() {
          var e = sr.get("scheduledAt"),
            t = sr.get("stoppedAt") || sr.get("deadline"),
            r = '\n    <div class="'.concat(Io.ready, '">\n      <div class="').concat(Io.description,
              '"><div>').concat(Ei("ready.description"), '</div></div>\n      <div class="').concat(Io
              .separator, '"></div>\n      <div class="').concat(Io.body, '">\n        <div class="').concat(
              Io.row, '">\n          <label class="').concat(Io.label, '">').concat(Ei("ready.nickname"),
              '</label>\n          <div class="').concat(Io.value, '">').concat(sr.get("student.nickname") ||
              sr.get("student.username"), '</div>\n        </div>\n        <div class="').concat(Io.row,
              '">\n          <label class="').concat(Io.label, '">').concat(Ei("ready.subject"),
              '</label>\n          <div class="').concat(Io.value, '">').concat(sr.get("subject") || sr.get(
              "identifier"), '</div>\n        </div>\n        <div class="').concat(Io.row, " ").concat(e ?
              "" : Io.hidden, '">\n          <label class="').concat(Io.label, '">').concat(Ei(
              "ready.scheduled"), '</label>\n          <div class="').concat(Io.value, '">').concat(new Date(
              e).toLocaleString(zi()), '</div>\n        </div>\n        <div class="').concat(Io.row, " ")
            .concat(t ? "" : Io.hidden, '">\n          <label class="').concat(Io.label, '">').concat(Ei(
              "ready.deadline"), '</label>\n          <div class="').concat(Io.value, '">').concat(new Date(t)
              .toLocaleString(zi()), '</div>\n        </div>\n        <div class="').concat(Io.error,
              '"></div>\n      </div>\n    </div>');
          return super.renderBody(r)
        }
        renderFooter() {
          return super.renderFooter({
            ok: Ei("ready.button.start"),
            disabled: this.params.disabled
          })
        }
        mounted() {
          super.mounted(), setTimeout(this.enable.bind(this), 1e3)
        }
        showError(e) {
          var t = this.$(Io.error);
          t.innerText = "", e && setTimeout((() => {
            var r = e.code || "ERR_SERVICE_UNAVAILABLE";
            t.innerText = Ei("ready.error.".concat(r)), this.enable()
          }), 1e3)
        }
        start(e) {
          this.disable();
          var t = this.params._callback;
          e ? sr.start().then((e => {
            this.remove(), t.call(this, e)
          })).catch((e => this.showError(e))) : (this.remove(), t.call(this, e))
        }
      }
      var Co = r(8365),
        zo = {};
      zo.styleTagTransform = ji(), zo.setAttributes = bi(), zo.insert = hi().bind(null, "head"), zo.domAPI =
      vi(), zo.insertStyleElement = yi();
      ui()(Co.Z, zo);
      const xo = Co.Z && Co.Z.locals ? Co.Z.locals : void 0;
  
      function Eo(e, t) {
        var r = Object.keys(e);
        if (Object.getOwnPropertySymbols) {
          var i = Object.getOwnPropertySymbols(e);
          t && (i = i.filter((function (t) {
            return Object.getOwnPropertyDescriptor(e, t).enumerable
          }))), r.push.apply(r, i)
        }
        return r
      }
  
      function So(e) {
        for (var t = 1; t < arguments.length; t++) {
          var r = null != arguments[t] ? arguments[t] : {};
          t % 2 ? Eo(Object(r), !0).forEach((function (t) {
            Oo(e, t, r[t])
          })) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object
            .getOwnPropertyDescriptors(r)) : Eo(Object(r)).forEach((function (t) {
            Object.defineProperty(e, t, Object.getOwnPropertyDescriptor(r, t))
          }))
        }
        return e
      }
  
      function Oo(e, t, r) {
        return t = function (e) {
          var t = function (e, t) {
            if ("object" != typeof e || null === e) return e;
            var r = e[Symbol.toPrimitive];
            if (void 0 !== r) {
              var i = r.call(e, t || "default");
              if ("object" != typeof i) return i;
              throw new TypeError("@@toPrimitive must return a primitive value.")
            }
            return ("string" === t ? String : Number)(e)
          }(e, "string");
          return "symbol" == typeof t ? t : String(t)
        }(t), t in e ? Object.defineProperty(e, t, {
          value: r,
          enumerable: !0,
          configurable: !0,
          writable: !0
        }) : e[t] = r, e
      }
      class Ro extends wn {
        constructor() {
          var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {};
          super(e), this.mount(e.el)
        }
        events() {
          var e = super.events();
          return e.click = So(So({}, e.click), {}, {
            [xo.checkbox]: (e, t) => {
              var r = t.querySelector("input");
              r.checked = !r.checked, r.checked ? this.enable() : this.disable()
            }
          }), e
        }
        renderBody() {
          var e = '<div class="'.concat(xo.content, '">');
          return this.params.label && (e += '<div class="'.concat(xo.label, '">').concat(this.params.label,
            "</div>")), this.params.text && (e += '<div class="'.concat(xo.text, '">').concat(this.params
            .text, "</div>")), this.params.checkbox && (e += '<div class="'.concat(xo.checkbox,
            '">\n      <span class="').concat(xo.caption, '">').concat(this.params.checkbox,
            '</span>\n      <input type="checkbox"><span class="').concat(xo.checkmark,
            '"></span>\n      </div>')), e += "</div>", super.renderBody(e)
        }
      }
      var Qo = r(9870),
        Yo = {};
      Yo.styleTagTransform = ji(), Yo.setAttributes = bi(), Yo.insert = hi().bind(null, "head"), Yo.domAPI =
      vi(), Yo.insertStyleElement = yi();
      ui()(Qo.Z, Yo);
      const Uo = Qo.Z && Qo.Z.locals ? Qo.Z.locals : void 0;
      class Go extends pn {
        constructor() {
          var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {};
          super(e), this.mount(e.el)
        }
        render() {
          var e = super.render();
          e.className = Uo.iframe;
          var t = l.get("iframe.allow") || "autoplay; microphone; camera; display-capture",
            r = l.get("iframe.sandbox") ? 'sandbox="'.concat(l.get("iframe.sandbox"), '"') : "";
          return e.innerHTML = '\n    <div class="'.concat(Uo.header, '" style="').concat(sr.hasAddon(
            "header") ? "" : "display:none", '">\n      <div class="').concat(Uo.btn, " ").concat(Uo
            .home_btn, '" title="').concat(Ei("iframe.button.home"), '"></div>\n      <div class="').concat(
            Uo.title, '">\n        <div><strong>').concat(sr.get("student.nickname") || sr.get(
            "student.username"), "</strong></div>\n        <div>").concat(sr.get("subject"),
            '</div>\n      </div>\n      <div class="').concat(Uo.btn, " ").concat(Uo.qrcode_btn,
            '" title="').concat(Ei("iframe.button.qrcode"), '" style="').concat(sr.hasAddon("qrcode") ? "" :
            "display:none", '"></div>\n      <div class="').concat(Uo.btn, " ").concat(Uo.calc_btn,
            '" title="').concat(Ei("iframe.button.calculator"), '" style="').concat(sr.hasAddon(
            "calculator") ? "" : "display:none", '"></div>\n      <div class="').concat(Uo.btn, " ").concat(
            Uo.chat_btn, '" title="').concat(Ei("iframe.button.chat"), '" style="').concat(sr.hasAddon(
            "chat") ? "" : "display:none", '"></div>\n      <button class="').concat(Uo.exit_btn,
            '" style="').concat(sr.hasAddon("finish") ? "" : "display:none", '">').concat(Ei(
            "iframe.button.finish"), '</button>\n    </div>\n    <iframe class="').concat(Uo.body,
            '" allow="').concat(t, '" ').concat(r, "></iframe>\n    "), e
        }
        getIframeURL() {
          if (sr.hasAddon("xapi")) {
            var e = new URL(sr.get("url")),
              t = {
                endpoint: Ee.url + "/api/xapi/",
                actor: JSON.stringify({
                  objectType: "Agent",
                  name: Re.get("nickname")
                }),
                activity_id: e.toString(),
                registration: sr.get("identifier")
              };
            return "".concat(e.origin).concat(e.pathname).concat(e.search ? e.search + "&" : "?").concat(
              new URLSearchParams(t), "&auth=Bearer ").concat(Ee.token).concat(e.hash)
          }
          return sr.get("url")
        }
        mounted() {
          var e = this.$(Uo.body);
          e.onload = function () {
            u.dispatchEvent("load", this)
          }, e.src = this.getIframeURL()
        }
        events() {
          return {
            click: {
              [Uo.home_btn]: () => {
                this.$(Uo.body).src = this.getIframeURL()
              },
              [Uo.exit_btn]: (e, t) => {
                this.params.onclick({
                  type: "exit",
                  target: t
                })
              },
              [Uo.chat_btn]: (e, t) => {
                this.params.onclick({
                  type: "chat",
                  target: t
                })
              },
              [Uo.calc_btn]: (e, t) => {
                this.params.onclick({
                  type: "calc",
                  target: t
                })
              },
              [Uo.qrcode_btn]: (e, t) => {
                this.params.onclick({
                  type: "qrcode",
                  target: t
                })
              }
            }
          }
        }
      }
      class Bo extends pn {
        constructor() {
          var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {};
          super(e);
          var t = l.get("inject");
          if (t) {
            var r = document,
              i = [];
            for (var n in Array.prototype.forEach.call(r.head.childNodes, (e => {
                i.push(e.outerHTML)
              })), t) {
              var o = t[n];
              if ("object" == typeof o) {
                var a = r.createElement(o.tagName);
                for (var s in o.innerHTML && (a.innerHTML = o.innerHTML), o)
                  if ("tagName" !== s && "innerHTML" !== s) try {
                    a.setAttribute(s, o[s])
                  } catch (e) {
                    console.error(e)
                  } - 1 === i.indexOf(a.outerHTML) && r.head.appendChild(a)
              }
            }
          }
          this.mount(e.el || document.body)
        }
        render() {
          Ci(Re.get("lang"));
          var e = super.render();
          return e.className = Li.proctoring, xi() && e.setAttribute("dir", "rtl"), e
        }
        renderCSS(e) {
          if ("string" == typeof e) this.el.classList.add(e);
          else if ("object" == typeof e)
            for (var t in e) this.el.style.setProperty(t, e[t])
        }
        mount(e) {
          return this.renderCSS(this.params.css || l.get("css")), super.mount(e)
        }
        mounted() {
          this._devtoolsHandler || (this._devtoolsHandler = this.devtoolsHandler.bind(this), u.on("devtools",
              this._devtoolsHandler)), this._startHandler || (this._startHandler = this.startHandler.bind(
              this), Ke.on("room:start", this._startHandler)), this._stopHandler || (this._stopHandler = this
              .stopHandler.bind(this), Ke.on("room:stop", this._stopHandler)), this._messageHandler || (this
              ._messageHandler = this.messageHandler.bind(this), Ke.on("chat:message", this._messageHandler)),
            this._metricsHandler || (this._metricsHandler = this.metricsHandler.bind(this), u.on("metrics",
              this._metricsHandler)), this._snapshotHandler || (this._snapshotHandler = this.snapshotHandler
              .bind(this), u.on("snapshot", this._snapshotHandler)), this._faceHandler || (this._faceHandler =
              this.faceHandler.bind(this), u.on("face", this._faceHandler)), this._receiverStartHandler || (
              this._receiverStartHandler = this.receiverStartHandler.bind(this))
        }
        removed() {
          this._devtoolsHandler && (u.off("devtools", this._devtoolsHandler), delete this._devtoolsHandler),
            this._startHandler && (Ke.off("room:start", this._startHandler), delete this._startHandler), this
            ._stopHandler && (Ke.off("room:stop", this._stopHandler), delete this._stopHandler), this
            ._messageHandler && (Ke.off("chat:message", this._messageHandler), delete this._messageHandler),
            this._metricsHandler && (u.off("metrics", this._metricsHandler), delete this._metricsHandler),
            this._snapshotHandler && (u.off("snapshot", this._snapshotHandler), delete this._snapshotHandler),
            this._faceHandler && (u.off("face", this._faceHandler), delete this._faceHandler), this
            ._receiverStartHandler && delete this._receiverStartHandler
        }
        init(e) {
          return new Promise((e => e())).then((() => this.close())).then((() => {
            if (!(Re.get("id") && !Re.hasRole("student") || sr.get("id"))) return new Promise(((t,
            r) => {
              var i = this;
              this._dialog = new Dn({
                el: this.el,
                payload: e,
                callback(e) {
                  if (delete i._dialog, e) t();
                  else {
                    var n = new Error("Session canceled by user");
                    n.code = "ERR_CANCELED_BY_USER", r(n)
                  }
                }
              })
            }))
          })).then((() => {
            if (!sr.get("startedAt")) return new Promise(((e, t) => {
              var r = this;
              this._dialog = new vo({
                el: this.el,
                callback(i) {
                  if (delete r._dialog, i) e();
                  else {
                    var n = new Error("Session canceled by user");
                    n.code = "ERR_CANCELED_BY_USER", t(n)
                  }
                }
              })
            }))
          }))
        }
        sync() {
          return this.init()
        }
        start() {
          return new Promise((e => e())).then((() => this.close())).then((() => sr.get("startedAt") && !sr
            .get("stoppedAt") || !sr.hasAddon("ready") ? sr.start() : new Promise(((e, t) => {
              var r = this;
              this._dialog = new Do({
                el: this.el,
                callback(i) {
                  if (delete r._dialog, i) e(i);
                  else {
                    var n = new Error("Session canceled by user");
                    n.code = "ERR_CANCELED_BY_USER", t(n)
                  }
                }
              })
            })))).then((e => {
            this._started = !0, Ke.join(e.id);
            var t = this._webcam = Xt({
                muted: !0,
                spinner: !0,
                mirror: !0
              }),
              r = sr.hasAddon("screen") && (this._screen = Xt({
                muted: !0
              })),
              i = this._conference = new yn({
                webcam: t,
                screen: r,
                restart: !0
              });
            i.on("receiver:start", this._receiverStartHandler);
            var n = this._chat = new jo({
                el: this.el,
                player: i.el,
                onincident: e => {
                  this._incident = e, this.lock(e)
                }
              }),
              o = this._calc = new wo({
                el: this.el
              });
            return sr.hasAddon(["toolbox", "preview"]) && (this._toolbar = new bo({
                el: this.el,
                onclick: e => {
                  switch (e.type) {
                  case "exit":
                    return this.finish();
                  case "qrcode":
                    return this.qrcode();
                  case "chat":
                    return n.toggle();
                  case "calc":
                    return o.toggle();
                  case "tooltip":
                    switch (e.target.dataset.id) {
                    case "c1":
                      return i.restart({
                        webcam: !0
                      });
                    case "s1":
                      return i.restart({
                        screen: !0
                      })
                    }
                  }
                }
              }), sr.hasAddon("preview") && this._toolbar.setVideo(t)), sr.hasAddon("content") &&
              Promise.all([un.start(), Oi.start()]), sr.hasAddon("lock") && (this.lock(!0), this
                ._firstlock = !0), i.start(e.id).then((() => (sr.get("url") && (this._iframe = new Go({
                el: this.el,
                onclick: e => {
                  switch (e.type) {
                  case "exit":
                    return this.finish();
                  case "qrcode":
                    return this.qrcode();
                  case "chat":
                    return n.toggle();
                  case "calc":
                    return o.toggle()
                  }
                }
              })), an.start(t, r), u.dispatchEvent("start", e))))
          })).then((() => {}))
        }
        stop() {
          return new Promise((e => e())).then((() => this.close())).then((() => sr.stop())).then((e => u
            .dispatchEvent("stop", e))).then((() => {}))
        }
        close() {
          return this.lock(!1), this._started && (Ke.leave(sr.get("id")), delete this._started), this
            ._iframe && (this._iframe.remove(), delete this._iframe), this._conference && (this._conference
              .remove(), delete this._conference), this._chat && (this._chat.remove(), delete this._chat),
            this._calc && (this._calc.remove(), delete this._calc), this._toolbar && (this._toolbar.remove(),
              delete this._toolbar), this._dialog && (this._dialog.remove(), delete this._dialog), Promise
            .all([un.stop(), Oi.stop(), an.stop()]).then((() => {}))
        }
        devtoolsHandler(e) {
          e.isOpen && (this.lock(!0), location.replace("about:blank"))
        }
        startHandler() {
          var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {},
            t = e.id,
            r = e.updatedAt;
          if (this._started && sr.get("id") === t && sr.get("updatedAt") !== r) return new Promise((e => e()))
            .then((() => this.close())).then((() => {
              this._dialog = new Ro({
                el: this.el,
                title: Ei("duplicate.title"),
                label: Ei("duplicate.label"),
                text: Ei("duplicate.text")
              })
            }))
        }
        stopHandler() {
          var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {},
            t = e.id,
            r = e.proctor;
          if (this._started && sr.get("id") === t) return new Promise((e => e())).then((() => this.close()))
            .then((() => {
              var t = Re.get("referrer") || "/";
              this._dialog = new Ro({
                el: this.el,
                title: Ei("finish.title"),
                label: Ei("finish.label"),
                text: Ei(r ? "finish.text.proctor" : "finish.text.auto"),
                ok: Ei("finish.button.ok"),
                callback() {
                  this.remove(), window.onbeforeunload = null, window.opener && window.close(),
                    location.href = t
                }
              }), u.dispatchEvent("stop", e)
            }))
        }
        messageHandler() {
          var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {};
          sr.get("id") === e.room && u.dispatchEvent("chat", e)
        }
        metricsHandler() {
          var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {};
          e.violated && e.peak ? this._violations = (this._violations || 0) + 1 : (this._violations = 0, this
            ._firstlock = !1);
          var t, r, i = this._violations > 1 || this._firstlock;
          (sr.hasAddon("lock") && this.lock(i), this._toolbar) && (e.violated && e.peak && (-1 !== ["c1",
              "s1"].indexOf(e.peak) && (r = e.peak), t = Ei("vision.events.".concat(e.peak))), this._toolbar
            .setText(t, r, i), this._toolbar.setHightlight(e.score));
          this._conference && this._conference.send(e)
        }
        snapshotHandler() {
          var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {};
          return Ee("/api/chat/".concat(sr.get("id")), {
            method: "POST",
            body: {
              type: "event",
              metadata: {
                metrics: e.metrics,
                weights: e.weights,
                peak: e.peak,
                score: e.score,
                threshold: e.threshold,
                violated: e.violated
              }
            }
          }).then((t => Promise.all(e.attach.map((e => Ee("/api/storage", {
            body: e
          }).catch((e => console.error(e)))))).then((function () {
            var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : [];
            return Ee("/api/chat/".concat(sr.get("id"), "/").concat(t.id), {
              method: "PUT",
              body: {
                attach: e.map((e => null == e ? void 0 : e.id)).filter((e => !!e))
              }
            })
          }))))
        }
        faceHandler() {
          var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {};
          return e.id && !sr.get("student.face") ? sr.update({
            student: {
              face: e.id
            }
          }) : Ee("/api/chat/".concat(sr.get("id")), {
            method: "POST",
            body: {
              type: "face",
              metadata: {
                distance: e.distance,
                threshold: e.threshold,
                similar: e.similar,
                verified: e.verified
              },
              attach: [e.id]
            }
          })
        }
        receiverStartHandler() {
          this._chat && this._chat.show()
        }
        qrcode() {
          if (this._dialog) return this._dialog.remove(), void delete this._dialog;
          var e = new wn({
              title: Ei("vision.qrcode"),
              close: !0,
              callback: () => e.remove()
            }),
            t = new po({
              el: e.renderBody(),
              onComplete: () => e.remove()
            });
          e.removed = () => {
            t && t.remove(), delete this._dialog
          }, this._dialog = e, e.mount(this.el)
        }
        lock(e) {
          e ? this.el.classList.add(Li.modal) : this._incident || this.el.classList.remove(Li.modal)
        }
        finish() {
          if (!this._dialog) {
            var e = this;
            this._dialog = new Ro({
              el: this.el,
              title: Ei("confirm.title"),
              label: Ei("confirm.label"),
              text: Ei("confirm.text"),
              ok: Ei("confirm.button.ok"),
              cancel: Ei("confirm.button.cancel"),
              checkbox: Ei("confirm.checkbox"),
              disabled: !0,
              callback(t) {
                if (delete e._dialog, this.remove(), t) {
                  var r = Re.get("referrer") || "/";
                  e.stop().then((() => {
                    window.onbeforeunload = null, window.opener && window.close(), location.href = r
                  }))
                }
              }
            })
          }
        }
      }
  
      function Ko(e, t) {
        var r = Object.keys(e);
        if (Object.getOwnPropertySymbols) {
          var i = Object.getOwnPropertySymbols(e);
          t && (i = i.filter((function (t) {
            return Object.getOwnPropertyDescriptor(e, t).enumerable
          }))), r.push.apply(r, i)
        }
        return r
      }
  
      function Ho(e) {
        for (var t = 1; t < arguments.length; t++) {
          var r = null != arguments[t] ? arguments[t] : {};
          t % 2 ? Ko(Object(r), !0).forEach((function (t) {
            qo(e, t, r[t])
          })) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object
            .getOwnPropertyDescriptors(r)) : Ko(Object(r)).forEach((function (t) {
            Object.defineProperty(e, t, Object.getOwnPropertyDescriptor(r, t))
          }))
        }
        return e
      }
  
      function qo(e, t, r) {
        return t = function (e) {
          var t = function (e, t) {
            if ("object" != typeof e || null === e) return e;
            var r = e[Symbol.toPrimitive];
            if (void 0 !== r) {
              var i = r.call(e, t || "default");
              if ("object" != typeof i) return i;
              throw new TypeError("@@toPrimitive must return a primitive value.")
            }
            return ("string" === t ? String : Number)(e)
          }(e, "string");
          return "symbol" == typeof t ? t : String(t)
        }(t), t in e ? Object.defineProperty(e, t, {
          value: r,
          enumerable: !0,
          configurable: !0,
          writable: !0
        }) : e[t] = r, e
      }
      class Wo {
        static get VERSION() {
          return "4.8.1-72f7e91"
        }
        get el() {
          return this._ui && this._ui.el
        }
        constructor() {
          var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {};
          this._options = e, this._ui = null, Ee.url = e.url || location.origin
        }
        on(e, t) {
          return u.on(e, t)
        }
        off(e, t) {
          return u.off(e, t)
        }
        emit(e, t) {
          return u.dispatchEvent(e, t)
        }
        init() {
          return ze(arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {}).then((e =>
            "signup" !== e.provider ? dr.login(e).then((() => e)) : e)).then((e => (this._ui = this._ui ||
            new Bo(this._options), this._ui.init(e).then((() => ({
              token: dr.token
            }))))))
        }
        sync() {
          var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {};
          return dr.sync(e).then((() => (this._ui = this._ui || new Bo(this._options), this._ui.sync().then((
          () => ({
            token: dr.token
          }))))))
        }
        start() {
          return new Promise(((e, t) => this._ui ? e() : t(new Error("Uninitialized")))).then((() => this._ui
            .start()))
        }
        stop() {
          return new Promise(((e, t) => this._ui ? e() : t(new Error("Uninitialized")))).then((() => this._ui
            .stop()))
        }
        close() {
          return new Promise(((e, t) => this._ui ? e() : t(new Error("Uninitialized")))).then((() => this._ui
            .close()))
        }
        logout() {
          var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {};
          return new Promise(((e, t) => this._ui ? e() : t(new Error("Uninitialized")))).then((() => this._ui
            .close())).then((() => (this._ui && (this._ui.remove(), this._ui = null), dr.logout()))).then((
            t => {
              var r = t.referrer;
              null != e && e.redirect && (window.onbeforeunload = null, window.opener && window.close()),
                !0 === (null == e ? void 0 : e.redirect) || !0 === e ? location.href = r || "/" :
                "string" == typeof (null == e ? void 0 : e.redirect) && (location.href = e.redirect)
            }))
        }
        lookup() {
          return Object.assign({}, Re.filter(...arguments), sr.filter(...arguments))
        }
        qrcode() {
          var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {};
          return dr.qrcode(e)
        }
        check(e) {
          return function (e) {
            return new Promise((e => e())).then((function () {
              if (!e || e.browser) return ri()
            })).then((function () {
              if (!e || e.camera) return ii()
            })).then((function () {
              if (!e || e.microphone) return ni()
            })).then((function () {
              if (!e || e.screen) return oi()
            })).then((function () {
              if (!e || e.network) return ai()
            })).then((function () {
              if (!e || e.webrtc) return si()
            }))
          }(e)
        }
        snapshot(e) {
          if (e instanceof HTMLVideoElement) return Ce(e, arguments.length > 1 && void 0 !== arguments[1] ?
            arguments[1] : {})
        }
        profile() {
          var e = [],
            t = (arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {}) || {},
            r = t.face,
            i = t.passport,
            n = {
              face: r,
              passport: i,
              nickname: t.nickname
            };
          return r instanceof File && e.push(this.upload(r, {
            type: "face",
            ref: Re.get("face")
          }).then((e => {
            n.face = e.id
          }))), i instanceof File && e.push(this.upload(i, {
            type: "passport",
            ref: Re.get("passport")
          }).then((e => {
            n.passport = e.id
          }))), Promise.all(e).then((() => sr.update({
            student: n
          })))
        }
        upload(e, t) {
          var r = t || {},
            i = r.filename,
            n = r.type,
            o = r.ref,
            a = r.nickname;
          return "string" == typeof e && (e = De(e, i)), t.face && (n = "face"), t.passport && (n =
            "passport"), Ee("/api/storage?type=".concat(n || "", "&ref=").concat(o || ""), {
            headers: "passport" === n && a ? {
              "x-passport-name": encodeURIComponent(a)
            } : {},
            body: e
          })
        }
      }
      var Vo = document.querySelector("script[data-supervisor]");
      if (Vo) {
        var Zo = Ho({}, Vo.dataset),
          Fo = Zo.supervisor || "start";
        delete Zo.supervisor;
        var Jo = function (e, t) {
            e = (e = e || window.location.search).split("+").join(" ");
            for (var r = {}, i = /[?&]([^=]+)=([^&]*)/g, n = i.exec(e); n;) r[decodeURIComponent(n[1])] =
              decodeURIComponent(n[2]), n = i.exec(e);
            return t ? r[t] : r
          }(),
          Xo = Jo.token,
          _o = Object.keys(Zo).length > 0;
        if (Xo || _o) {
          var $o = (new URL(Vo.src) || {}).origin,
            ea = new Wo({
              url: $o
            });
          (_o ? ea.init(Ho({}, Zo)) : ea.sync({
            token: Xo
          })).then((function () {
            if ("init" !== Fo) return ea.start()
          })).catch((function (e) {
            console.error(e), window.opener && window.close(), location.href = Zo.referrer || Re.get(
              "referrer") || "/"
          })), window.supervisor = ea
        }
      }
    })(), i = i.default
  })()));