function getImagePath(name) {
  if (process.env.NODE_ENV === 'development') {
    return `/assets/${name}`;
  }
  return `/static-assets/${name}`;
}

function getApiUrl() {
  if (process.env.NODE_ENV === 'development') {
    // Local flask development server
    return 'http://127.0.0.1:5000/api';
  }

  // In production, the api url is the same as the current
  // location. It is just extended by /api.
  return '/api';
}

function resolveLandClassNames(string) {
  if (!string) return null;
  if (string === 'WENS') return 'All';

  const classNames = [];
  string.split('').forEach((letter) => {
    // Land Base Classes
    if (letter === 'W') classNames.push('Mercenary');
    if (letter === 'E') classNames.push('Explorer');
    if (letter === 'N') classNames.push('Noble');
    if (letter === 'S') classNames.push('Saint');
    // Land CC Classes
    if (letter === 'P') classNames.push('Priest');
    if (letter === 'A') classNames.push('Shaman');
    if (letter === 'G') classNames.push('Gladiator');
    if (letter === 'D') classNames.push('Guardian Swordsman');
    if (letter === 'M') classNames.push('Court Magician');
    if (letter === 'K') classNames.push('Magic Knight');
    if (letter === 'B') classNames.push('Excavator');
    if (letter === 'H') classNames.push('Sniper');
  });

  return classNames.join(', ');
}

function resolveSeaClassNames(string) {
  if (!string) return null;
  if (string === 'ARGHM') return 'All';

  const classNames = [];
  string.split('').forEach((letter) => {
    // Sea classes
    if (letter === 'A') classNames.push('Armored Ship');
    if (letter === 'G') classNames.push('Big Gun Ship');
    if (letter === 'H') classNames.push('Torpedo Ship');
    if (letter === 'M') classNames.push('Mainteance Ship');
    if (letter === 'R') classNames.push('Assault Ship');
  });

  return classNames.join(', ');
}

function tablenameToTitle(tablename) {
  const parts = [];

  tablename.split('_').forEach((part) => {
    parts.push(part[0].toUpperCase() + part.slice(1));
  });

  return parts.join(' ');
}

function resolveBoolToString(value) {
  return value ? 'Yes' : 'No';
}

function resolveWeaponTypeToName(letters) {
  const weaponNames = [];

  letters.split('').forEach((type) => {
    if (type === 'P') weaponNames.push('Duals');
    if (type === 'R') weaponNames.push('Rifle');
    if (type === 'C') weaponNames.push('Cariad');
    if (type === 'B') weaponNames.push('Shield');
    if (type === 'A') weaponNames.push('Rapier');
    if (type === 'T') weaponNames.push('Two-handed Sword');
    if (type === 'S') weaponNames.push('One-handed Sword');
    if (type === 'D') weaponNames.push('Dagger');
    if (type === 'F') weaponNames.push('Fishing Rod');
    if (type === 'X') weaponNames.push('All Weapons');
  });

  return weaponNames.join(', ');
}

function getEffectStrings(effects) {
  const effectStrings = [];

  effects.forEach((effect) => {
    const effectName = effect.code.name;
    let { operator, value } = effect;

    // Replace e.g. Max HP + -50 to ... - 50
    if (value < 0) {
      operator = '-';
      value *= -1;
    }

    if (operator === '*') {
      effectStrings.push(`${effectName} ${Math.round(value * 100)}%`);
    } else {
      effectStrings.push(`${effectName} ${operator}${value}`);
    }
  });

  return effectStrings;
}

function getDurationString(duration) {
  // Given duration is in minutes
  const minutes = duration - 1; // duration always has 1 second more..

  const hours = (minutes / 24);
  const days = (hours / 60);

  if (days >= 1) {
    return `${days} Days`;
  }
  if (hours >= 1) {
    return `${minutes} Minutes`;
  }
  return `${hours} Hours`;
}

function formatTextLinebreaks(text) {
  return text.split('\\n').join('\n');
}

function getRareGradeFromItem(tablename, item) {
  if (tablename === 'monster') {
    if (item.rating) {
      return item.rating.value;
    }
    return -1;
  }
  if (tablename === 'quest' || tablename === 'npc') return -1;
  return item.rare_grade;
}

function setWindowTitle(title) {
  document.title = `${title} | Flandria`;
}

export {
  getImagePath,
  getApiUrl,
  resolveLandClassNames,
  resolveSeaClassNames,
  tablenameToTitle,
  resolveBoolToString,
  getEffectStrings,
  getDurationString,
  formatTextLinebreaks,
  getRareGradeFromItem,
  resolveWeaponTypeToName,
  setWindowTitle,
};
