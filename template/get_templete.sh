#!/usr/bin/env bash
set -euo pipefail

SCRIPT_NAME=$(basename "${BASH_SOURCE[0]:-$0}")
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)

DEFAULT_REPO_URL="https://github.com/example/example.git"

# Color setup ---------------------------------------------------------------
if [[ -t 1 ]]; then
  if command -v tput >/dev/null 2>&1; then
    COLOR_SUPPORT=$(tput colors 2>/dev/null || echo 0)
  else
    COLOR_SUPPORT=0
  fi
else
  COLOR_SUPPORT=0
fi

if [[ $COLOR_SUPPORT -ge 8 ]]; then
  RED="$(tput setaf 1)"
  GREEN="$(tput setaf 2)"
  YELLOW="$(tput setaf 3)"
  BLUE="$(tput setaf 4)"
  MAGENTA="$(tput setaf 5)"
  CYAN="$(tput setaf 6)"
  RESET="$(tput sgr0)"
else
  RED=""
  GREEN=""
  YELLOW=""
  BLUE=""
  MAGENTA=""
  CYAN=""
  RESET=""
fi

log_step()    { printf "%b==>%b %s\n" "$CYAN" "$RESET" "$1"; }
log_info()    { printf "%b[i]%b %s\n" "$BLUE" "$RESET" "$1"; }
log_warn()    { printf "%b[!]%b %s\n" "$YELLOW" "$RESET" "$1"; }
log_error()   { printf "%b[x]%b %s\n" "$RED" "$RESET" "$1"; }
log_success() { printf "%b[✓]%b %s\n" "$GREEN" "$RESET" "$1"; }

usage() {
  cat <<EOF
${CYAN}Usage${RESET}: ${SCRIPT_NAME} [REPO_URL] [TARGET_DIR]

REPO_URL   Git repository to clone (default: ${DEFAULT_REPO_URL})
TARGET_DIR Directory name to create (default: repo name, inside script directory)

Examples:
  ${SCRIPT_NAME}
  ${SCRIPT_NAME} https://github.com/my-org/my-app.git
  ${SCRIPT_NAME} https://github.com/my-org/my-app.git ./custom-folder
EOF
}

# Parse input ---------------------------------------------------------------
REPO_URL="${1:-$DEFAULT_REPO_URL}"
if [[ "${REPO_URL}" == "-h" || "${REPO_URL}" == "--help" ]]; then
  usage
  exit 0
fi

DEFAULT_DEST="${SCRIPT_DIR}/$(basename "${REPO_URL%.git}")"
TARGET_DIR="${2:-$DEFAULT_DEST}"

log_step "Starting clone helper"
log_info "Script directory: ${SCRIPT_DIR}"
log_info "Repository URL   : ${REPO_URL}"
log_info "Target directory : ${TARGET_DIR}"

# Checks --------------------------------------------------------------------
if ! command -v git >/dev/null 2>&1; then
  log_error "Git is not installed. Please install Git and retry."
  exit 1
fi
log_success "Git detected: $(git --version)"

if [[ -e "${TARGET_DIR}" ]]; then
  log_warn "Target directory already exists."
  read -r -p "Overwrite ${TARGET_DIR}? [y/N] " response
  case "${response}" in
    [yY][eE][sS]|[yY])
      log_warn "Removing existing directory..."
      rm -rf "${TARGET_DIR}"
      ;;
    *)
      log_error "Aborting to avoid overwriting existing directory."
      exit 1
      ;;
  esac
fi

# Clone ---------------------------------------------------------------------
log_step "Cloning repository..."
git clone "${REPO_URL}" "${TARGET_DIR}"
log_success "Repository cloned into ${TARGET_DIR}"

# Post-clone summary --------------------------------------------------------
log_step "Summary"
log_info "Repository : ${REPO_URL}"
log_info "Location   : ${TARGET_DIR}"
log_success "Done! You can now explore your project."