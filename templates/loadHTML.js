function loadHTML(file) {
    var rawFile = new XMLHttpRequest();
    rawFile.open("GET", file, false);
    rawFile.onreadystatechange = function () {
      if (rawFile.readyState === 4) {
        if (rawFile.status === 200 || rawFile.status == 0) {
          var allText = rawFile.responseText;
          document.write(allText);
        }
      }
    };
    rawFile.send(null);
  }
  
  const logoutBtn = document.querySelector("#logout");
  const logout = () => {
    localStorage.removeItem("refreshToken");
    localStorage.removeItem("token");
    localStorage.removeItem("loggedin");
    alert("로그아웃되었습니다!");
    window.location.href = "/";
  };