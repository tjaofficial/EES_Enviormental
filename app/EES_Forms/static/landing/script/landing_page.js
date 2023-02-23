//var t=setInterval(runFunction,1000);
document.getElementById('dot1').addEventListener('click', change1);
document.getElementById('dot2').addEventListener('click', change2);
document.getElementById('dot3').addEventListener('click', change3);

function change1(){
    const cover1 = document.getElementById('cover1'),
    cover2 = document.getElementById('cover2'),
    cover3 = document.getElementById('cover3'),
    dot1 = document.getElementById('dot1'),
    dot2 = document.getElementById('dot2'),
    dot3 = document.getElementById('dot3');

    cover1.style.display = 'flex';
    cover2.style.display = 'none';
    cover3.style.display = 'none';

    dot1.style.backgroundColor = '#29333691';
    dot2.style.backgroundColor = '#c1d5da';
    dot3.style.backgroundColor = '#c1d5da';
}
function change2(){
    const cover1 = document.getElementById('cover1'),
    cover2 = document.getElementById('cover2'),
    cover3 = document.getElementById('cover3'),
    dot1 = document.getElementById('dot1'),
    dot2 = document.getElementById('dot2'),
    dot3 = document.getElementById('dot3');

    cover1.style.display = 'none';
    cover2.style.display = 'flex';
    cover3.style.display = 'none';

    dot1.style.backgroundColor = '#c1d5da';
    dot2.style.backgroundColor = '#29333691';
    dot3.style.backgroundColor = '#c1d5da';
}
function change3(){
    const cover1 = document.getElementById('cover1'),
    cover2 = document.getElementById('cover2'),
    cover3 = document.getElementById('cover3'),
    dot1 = document.getElementById('dot1'),
    dot2 = document.getElementById('dot2'),
    dot3 = document.getElementById('dot3');

    cover1.style.display = 'none';
    cover2.style.display = 'none';
    cover3.style.display = 'flex';

    dot1.style.backgroundColor = '#c1d5da';
    dot2.style.backgroundColor = '#c1d5da';
    dot3.style.backgroundColor = '#29333691';
}